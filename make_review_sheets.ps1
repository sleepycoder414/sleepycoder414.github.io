param([string]$Pattern='*example*.png',[string]$Suffix='examples')
Add-Type -AssemblyName System.Drawing
$reviewRoot = Join-Path $PSScriptRoot 'review'
New-Item -ItemType Directory -Force -Path $reviewRoot | Out-Null
foreach($styleDir in Get-ChildItem -LiteralPath $PSScriptRoot -Directory -Filter 'style_*') {
 $files=@(Get-ChildItem -LiteralPath $styleDir.FullName -File -Filter $Pattern)
 if($files.Count -eq 0){continue}
 $sheet=[System.Drawing.Bitmap]::new(1500,([int][Math]::Ceiling($files.Count/3.0)*370))
 $g=[System.Drawing.Graphics]::FromImage($sheet)
 $g.Clear([System.Drawing.Color]::White)
 $font=[System.Drawing.Font]::new('Arial',12)
 for($i=0;$i -lt $files.Count;$i++) {
  $im=[System.Drawing.Image]::FromFile($files[$i].FullName)
  $x=($i%3)*500; $y=[int][Math]::Floor($i/3)*370
  $scale=[Math]::Min(490.0/$im.Width,330.0/$im.Height)
  $g.DrawImage($im,[int]$x,[int]$y,[int]($im.Width*$scale),[int]($im.Height*$scale))
  $g.DrawString($files[$i].Name,$font,[System.Drawing.Brushes]::Black,[single]$x,[single]($y+335))
  $im.Dispose()
 }
 $sheet.Save((Join-Path $reviewRoot ($styleDir.Name+'_'+$Suffix+'.jpg')),[System.Drawing.Imaging.ImageFormat]::Jpeg)
 $font.Dispose(); $g.Dispose(); $sheet.Dispose()
}
