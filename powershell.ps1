Param($file, $fullpath)
$word = NEW-OBJECT -COMOBJECT WORD.APPLICATION

#try 
#{
    #$doc = $word.Documents.OpenNoRepairDialog($file.FullName)
    #$doc.SaveAs([ref] $file.FullName.Replace(".doc",".pdf"),[ref] 17)
    #$doc.Close()
    #Write-Host "$($file.FullName)をPDF変換しました"        
#}
#catch
#{
    #Write-Host "[ERROR]$($file.FullName)のPDF変換に失敗しました"
#}


try 
{
    Write-Host "$($file)"
    $doc = $word.Documents.OpenNoRepairDialog($fullpath)
    Write-Host "$($doc))"
    $test = $fullpath.Replace(".docx",".pdf")
    Write-Host "$($test)"
    $doc.SaveAs([ref] $fullpath.Replace(".docx",".pdf"),[ref] 17)
    $doc.Close()    
}
catch
{
    Write-Host "[ERROR]$($file)のPDF変換に失敗しました"
}

$word.Quit()