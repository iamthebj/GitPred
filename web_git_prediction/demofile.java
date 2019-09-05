import java.io.*;  
public class demofile {  
    public static void main(String[] args) {  
  
        try {  
            File file = new File("javaFile123.txt")  
            if (file.createNewFile()) {  
                System.out.println("New File is created")
            } els {
                System.out.println("File already exists.");  
            }  
        } ctch (IOException e) {  
            e.printStackTrace() 
        }  
  
    }  
}  
