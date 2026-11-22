$env:PIP_CACHE_DIR='D:\Dev\pip_cache'
$env:TEMP='D:\Dev\tmp'
$ErrorActionPreference='Stop'
$taskRoot=Split-Path $PSScriptRoot -Parent
$docxPath=Join-Path $taskRoot 'phase3_output\report\Milestone3_Final.docx'
$pdfPath=Join-Path $taskRoot 'phase3_output\report\Milestone3_Final.pdf'
$wordApp=New-Object -ComObject Word.Application
$wordApp.Visible=$false
$wordApp.DisplayAlerts=0
try {
  $reportDoc=$wordApp.Documents.Open($docxPath,$false,$false)
  $reportDoc.Fields.Update() | Out-Null
  $reportDoc.Repaginate()
  $reportDoc.Save()
  $reportDoc.ExportAsFixedFormat($pdfPath,17)
  Write-Output ('Word PDF export completed; pages: '+$reportDoc.ComputeStatistics(2))
  $reportDoc.Close(0)
} finally { $wordApp.Quit() }
