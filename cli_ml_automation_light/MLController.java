import java.io.*;  
public class MLController {  
  
  public static void main(String argv[]) {  
    try {  
      String line;  
      String currentDirectory=System.getProperty("user.dir");
      String invoke="python \""+currentDirectory+"/ml_automation/core/AutomationProcessor.py\"  \""+currentDirectory+"\"";
      String invokeArgument=" \"{'custom_function_object':{'request_id':'1','request_shortname':'function_1','python_function':'ml_automation.custom_functions.custom_function.DummyCustomTemplate.performOperation','arguments':{}}}\"";
      String command=invoke+invokeArgument;
      System.out.println("Input\n"+command+"\n");
      Process p = Runtime.getRuntime().exec(command);  
      BufferedReader input = new BufferedReader(new InputStreamReader(p.getInputStream()));  
      while ((line = input.readLine()) != null) {  
        System.out.println("Output\n"+line+"\n");  
      }  
      input.close();  
    }  
    catch (Exception err) {  
      err.printStackTrace();  
    }  
  }  
}