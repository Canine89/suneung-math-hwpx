# Hangul COM automation: open hwpx -> (refresh equations) -> save hwpx/pdf
param(
  [Parameter(Mandatory=$true)][string]$In,
  [string]$OutHwpx = "",
  [string]$OutPdf = "",
  [switch]$RefreshEquations
)
$hwp = New-Object -ComObject HWPFrame.HwpObject
try {
  $hwp.XHwpWindows.Item(0).Visible = $false
  Write-Output ("security module: " + $hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModuleExample"))
  $ok = $hwp.Open($In, "HWPX", "forceopen:true")
  if (-not $ok) { throw "open failed: $In" }
  if ($RefreshEquations) {
    $n = 0
    $ctrl = $hwp.HeadCtrl
    while ($ctrl -ne $null) {
      if ($ctrl.CtrlID -eq "eqed") {
        $p = $ctrl.Properties
        $script = $p.Item("String")
        $p.SetItem("String", $script)
        $ctrl.Properties = $p
        $n++
      }
      $ctrl = $ctrl.Next
    }
    Write-Output "equations refreshed: $n"
  }
  if ($OutHwpx) { Write-Output ("hwpx: " + $hwp.SaveAs($OutHwpx, "HWPX", "")) }
  if ($OutPdf)  { Write-Output ("pdf: "  + $hwp.SaveAs($OutPdf, "PDF", "")) }
} finally {
  try { $hwp.Quit() } catch {}
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($hwp)
}
