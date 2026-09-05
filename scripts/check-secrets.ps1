$ErrorActionPreference = 'Stop'

$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$tracked = git -C $repositoryRoot ls-files --cached --others --exclude-standard
$patterns = @(
  '(?i)(api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*["''][^"'']{8,}',
  'gh[opusr]_[A-Za-z0-9_]{20,}',
  '-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----',
  '(?i)C:\\Users\\[^\\]+\\',
  'https://docs\.google\.com/spreadsheets/d/[A-Za-z0-9_-]+'
)

$violations = New-Object System.Collections.Generic.List[string]
foreach ($relativePath in $tracked) {
  $fullPath = Join-Path $repositoryRoot $relativePath
  if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) { continue }
  if ([System.IO.Path]::GetExtension($fullPath) -in @('.png', '.jpg', '.jpeg', '.gif', '.webp')) { continue }
  foreach ($pattern in $patterns) {
    if (Select-String -LiteralPath $fullPath -Pattern $pattern -Quiet -ErrorAction SilentlyContinue) {
      $violations.Add($relativePath)
      break
    }
  }
}

if ($violations.Count -gt 0) {
  Write-Error ('Potential secret or private path detected in: ' + (($violations | Sort-Object -Unique) -join ', '))
}

Write-Output ('Secret and private-path scan passed for {0} files.' -f $tracked.Count)
