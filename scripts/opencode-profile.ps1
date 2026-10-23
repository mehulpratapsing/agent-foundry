param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('superpowers', 'ecc', 'gstack', 'research', 'security', 'memory')]
    [string]$Profile,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$OpenCodeArgs
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$profileConfig = Join-Path $repoRoot "profiles/$Profile.json"
if (-not (Test-Path -LiteralPath $profileConfig)) {
    throw "Profile config not found: $profileConfig"
}

$previousConfig = $env:OPENCODE_CONFIG
Push-Location $repoRoot
try {
    $env:OPENCODE_CONFIG = $profileConfig
    & opencode @OpenCodeArgs
}
finally {
    Pop-Location
    if ($null -eq $previousConfig) {
        Remove-Item Env:OPENCODE_CONFIG -ErrorAction SilentlyContinue
    }
    else {
        $env:OPENCODE_CONFIG = $previousConfig
    }
}
