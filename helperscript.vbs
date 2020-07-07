Option Explicit

Dim fsShell,i

Set fsShell = WScript.CreateObject("WScript.Shell")
WScript.Sleep 1000

For i=1 To 1
fsShell.SendKeys "{ENTER}" 
'fsShell.SendKeys ("^{Esc}")
WScript.Sleep 1000
Next

'WScript.Echo
