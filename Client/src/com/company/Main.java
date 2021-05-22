package com.company;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ConnectException;
import java.net.Socket;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) throws IOException {
        connection();
    }
    public static void connection() throws IOException {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Give server IP address: ");
        Socket s = new Socket(scanner.nextLine(),6000);
        PrintWriter pr = new PrintWriter(s.getOutputStream());
        InputStreamReader in = new InputStreamReader(s.getInputStream());
        BufferedReader bf = new BufferedReader(in);

        String str=bf.readLine();
        if(str.equals("CONNECTED")){
            System.out.println("You are connected with Game server");
        }else throw new ConnectException();

        System.out.print("Type your name: ");
        pr.print(scanner.nextLine());
        pr.flush();

        label:
        while(true) {
            String server = bf.readLine();
            switch (server) {
                case "WAIT":
                    System.out.println("We are still waiting for other players");
                    break;
                case "YOURDIGIT":
                    while (true) {
                        System.out.print("SERVER: Give your guess: ");
                        int myGuess = scanner.nextInt();
                        if (myGuess >= 1 && myGuess <= 6) {
                            pr.print(myGuess);
                            pr.flush();
                            break;
                        }
                    }
                    break;
                case "WRONG":
                    System.out.print("SERVER: Not what i have on mind. My number was: ");
                    System.out.println(bf.read() - 48);
                    break;
                case "GOOD":
                    System.out.println("SERVER: Congratulations that was right number!");
                    break;
                case "GG":
                    System.out.println("SERVER: We have winner GG!");
                    break label;
                default:
                    break label;
            }
        }

        pr.close();
        s.close();
    }
}
