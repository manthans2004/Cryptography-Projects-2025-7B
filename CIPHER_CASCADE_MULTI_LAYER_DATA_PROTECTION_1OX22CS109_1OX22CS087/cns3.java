Code: 
 
package nanducns; 
import java.util.Scanner; 
public class Cns3 { 
     static int modInverse(int a, int m) { 
         a = ((a % m) + m) % m; 
         for (int x = 1; x < m; x++) if ((a * x) % m == 1) return x; 
         throw new ArithmeticException("No modular inverse found"); 
     } 
 
     static int[][] hillInverse(int[][] key) { 
         int n = key.length; 
         int det = 0; 
         if (n == 2) det = key[0][0]*key[1][1] - key[0][1]*key[1][0]; 
         else if (n == 3) { 
             det += key[0][0]*(key[1][1]*key[2][2]-key[1][2]*key[2][1]); 
             det -= key[0][1]*(key[1][0]*key[2][2]-key[1][2]*key[2][0]); 
             det += key[0][2]*(key[1][0]*key[2][1]-key[1][1]*key[2][0]); 
         } 
         det = ((det%26)+26)%26; 
         int detInv = modInverse(det,26); 
 
         int[][] adj = new int[n][n]; 
         if(n==2){ 
             adj[0][0]=key[1][1]; adj[0][1]=-key[0][1]; 
             adj[1][0]=-key[1][0]; adj[1][1]=key[0][0]; 
         } else if(n==3){ 
             adj[0][0]= key[1][1]*key[2][2] - key[1][2]*key[2][1]; 
             adj[0][1]= -(key[0][1]*key[2][2] - key[0][2]*key[2][1]); 
             adj[0][2]= key[0][1]*key[1][2] - key[0][2]*key[1][1]; 
             adj[1][0]= -(key[1][0]*key[2][2] - key[1][2]*key[2][0]); 
             adj[1][1]= key[0][0]*key[2][2] - key[0][2]*key[2][0]; 
             adj[1][2]= -(key[0][0]*key[1][2] - key[0][2]*key[1][0]); 
             adj[2][0]= key[1][0]*key[2][1] - key[1][1]*key[2][0]; 
             adj[2][1]= -(key[0][0]*key[2][1] - key[0][1]*key[2][0]); 
             adj[2][2]= key[0][0]*key[1][1] - key[0][1]*key[1][0]; 
         } 
 
         int[][] inv = new int[n][n]; 
         for(int i=0;i<n;i++) 
             for(int j=0;j<n;j++) 
                 inv[i][j]=((adj[i][j]*detInv)%26 +26)%26; 
         return inv; 
     } 
 
     static String hillEncrypt(String text,int[][] key){ 
         StringBuilder cipher=new StringBuilder(); 
         int n=key.length; 
         System.out.println("\n--- Hill Cipher Encryption ---"); 
         String lettersOnly=text.toUpperCase().replaceAll("[^A-Z]",""); 
         while(lettersOnly.length()%n!=0) lettersOnly+="X"; 
 
         for(int i=0;i<lettersOnly.length();i+=n){ 
             int[] block=new int[n]; 
             for(int j=0;j<n;j++) block[j]=lettersOnly.charAt(i+j)-'A'; 
             int[] enc=new int[n]; 
             for(int r=0;r<n;r++){ 
                 enc[r]=0; 
                 for(int c=0;c<n;c++) enc[r]+=key[r][c]*block[c]; 
                 enc[r]=((enc[r]%26)+26)%26; 
             } 
             for(int j=0;j<n;j++){ 
                 System.out.println((char)(block[j]+'A') + " -> " + 
(char)(enc[j]+'A')); 
                 cipher.append((char)(enc[j]+'A')); 
             } 
         } 
         return cipher.toString(); 
     } 
 
     static String hillDecrypt(String text,int[][] key){ 
         int[][] invKey=hillInverse(key); 
         int n=key.length; 
         StringBuilder plain=new StringBuilder(); 
         System.out.println("\n--- Hill Cipher Decryption ---"); 
         for(int i=0;i<text.length();i+=n){ 
             int[] block=new int[n]; 
             for(int j=0;j<n;j++) block[j]=text.charAt(i+j)-'A'; 
             int[] dec=new int[n]; 
             for(int r=0;r<n;r++){ 
                 dec[r]=0; 
                 for(int c=0;c<n;c++) dec[r]+=invKey[r][c]*block[c]; 
                 dec[r]=((dec[r]%26)+26)%26; 
             } 
             for(int j=0;j<n;j++){ 
                 System.out.println((char)(block[j]+'A') + " -> " + 
(char)(dec[j]+'A')); 
                 plain.append((char)(dec[j]+'A')); 
             } 
         } 
         return plain.toString(); 
     } 
 
     static String caesarEncrypt(String text,int shift){ 
         StringBuilder res=new StringBuilder(); 
         System.out.println("\n--- Caesar Cipher Encryption ---"); 
         for(char c:text.toCharArray()){ 
             char e=(char)((c-'A'+shift)%26+'A'); 
             System.out.println(c + " -> " + e); 
             res.append(e); 
         } 
         return res.toString(); 
     } 
 
     static String caesarDecrypt(String text,int shift){ 
         StringBuilder res=new StringBuilder(); 
         System.out.println("\n--- Caesar Cipher Decryption ---"); 
         for(char c:text.toCharArray()){ 
             char d=(char)((c-'A'-shift+26)%26+'A'); 
             System.out.println(c + " -> " + d); 
             res.append(d); 
         } 
         return res.toString(); 
     } 
 
     static String otpEncrypt(String text,int[] otp){ 
         StringBuilder cipher=new StringBuilder(); 
         System.out.println("\n--- OTP Encryption ---"); 
         for(int i=0;i<text.length();i++){ 
             char otpChar=(char)(otp[i]+'A'); 
             char e=(char)((text.charAt(i)-'A'+otpChar-'A')%26+'A'); 
             System.out.println(text.charAt(i) + " + " + otpChar + " -> " + 
e); 
             cipher.append(e); 
         } 
         return cipher.toString(); 
     } 
 
     static String otpDecrypt(String text,int[] otp){ 
         StringBuilder plain=new StringBuilder(); 
         System.out.println("\n--- OTP Decryption ---"); 
         for(int i=0;i<text.length();i++){ 
             char otpChar=(char)(otp[i]+'A'); 
             char d=(char)((text.charAt(i)-'A'- (otpChar-'A') +26)%26+'A'); 
             System.out.println(text.charAt(i) + " - " + otpChar + " -> " + 
d); 
             plain.append(d); 
         } 
         return plain.toString(); 
     } 
 
     public static void main(String[] args){ 
         Scanner sc=new Scanner(System.in); 
 
         System.out.println("Enter plaintext:"); 
         String plaintext=sc.nextLine(); 
 
         System.out.println("Enter Hill key size (2 or 3):"); 
         int n=sc.nextInt(); 
         int[][] hillKey=new int[n][n]; 
         System.out.println("Enter Hill key matrix row-wise:"); 
         for(int i=0;i<n;i++) for(int j=0;j<n;j++) 
hillKey[i][j]=sc.nextInt(); 
 
         System.out.println("Enter Caesar shift:"); 
         int shift=sc.nextInt(); 
 
         int lettersOnlyCount=plaintext.toUpperCase().replaceAll("[^A
Z]","").length(); 
         int[] otpKey=new int[lettersOnlyCount]; 
         System.out.println("Enter OTP key as numbers (0-25), one for each 
letter in plaintext:"); 
         for(int i=0;i<lettersOnlyCount;i++){ 
             otpKey[i]=sc.nextInt(); 
             if(otpKey[i]<0 || otpKey[i]>25){ 
                 System.out.println("Invalid OTP number! Must be 0-25"); 
                 return; 
             } 
         } 
 
         // --- Hill Cipher --- 
         String hillEnc=hillEncrypt(plaintext,hillKey); 
 
         // 
         String caesarEnc=caesarEncrypt(hillEnc,shift); 
 
// --- OTP Encryption --- 
String otpEnc=otpEncrypt(caesarEnc,otpKey); 
System.out.println("\nEncrypted Cipher Text: " + otpEnc); 
String otpDec=otpDecrypt(otpEnc,otpKey); 
String caesarDec=caesarDecrypt(otpDec,shift); 
String finalPlain=hillDecrypt(caesarDec,hillKey); 
System.out.println("\nFinal Decrypted Plaintext: " + finalPlain); 
} 
} 