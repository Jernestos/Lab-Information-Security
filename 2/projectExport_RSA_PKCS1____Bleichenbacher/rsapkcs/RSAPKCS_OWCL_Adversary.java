package rsapkcs;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Random;

import static utils.NumberUtils.getRandomBigInteger;
import static utils.NumberUtils.ceilDivide;
import static utils.NumberUtils.getCeilLog;

import java.util.*;

public class RSAPKCS_OWCL_Adversary implements I_RSAPKCS_OWCL_Adversary {
    public RSAPKCS_OWCL_Adversary() {
        // Do not change this constructor!
    }

    /*
     * @see basics.IAdversary#run(basics.IChallenger)
     */
     
    public Boolean oracle(BigInteger c) {
      try {
        this.query_counter++;
        if (this.debug_mode) {
          if (this.query_counter % 10000 == 0) {
            System.out.print("Query call: ");
            System.out.println(this.query_counter);
          }
        }
        return this.challenger_.isPKCSConforming(c);
      } 
      catch (Exception error) {
        System.out.print("Exception caught: ");
        System.out.println(error);
        return true; //or else we are stuck in inf loop, the outer loop in run will cause the program to terminate because the running condition is no longer satisfied
      }
    }
    
    public long query_counter;
    public long max_queryQuota;
    public BigInteger m;
    
    public I_RSAPKCS_OWCL_Challenger challenger_;
    
    // public HashSet<BigInteger[]> union(HashSet<BigInteger[]> M, BigInteger a, BigInteger b) {
    //   Iterator<BigInteger[]> M_iterator = M.iterator();
    //   HashSet<BigInteger[]> new_M = new HashSet<BigInteger[]>();
    //   while (M_iterator.hasNext()) {
    //     BigInteger[] temp_list = M_iterator.next();
    //     if (temp_list[0].compareTo(b) <= 0 && a.compareTo(temp_list[1]) <= 0) {
    //       a = a.min(temp_list[0]);
    //       b = b.max(temp_list[1]);
    //       BigInteger[] new_list_M = new BigInteger[2];
    //       new_list_M[0] = a;
    //       new_list_M[1] = b;
    //       new_M.add(new_list_M);
    //     }
    //   }
    //   BigInteger[] new_list_M = new BigInteger[2];
    //   new_list_M[0] = a;
    //   new_list_M[1] = b;
    //   new_M.add(new_list_M);
    //   return new_M;
    // }
    
    public ArrayList<BigInteger[]> check_overlap(ArrayList<BigInteger[]> M, BigInteger a, BigInteger b) {
      
      
      
      for (int i = 0; i < M.size(); ++i) {
        BigInteger[] interval = M.get(i);
        if (interval[0].compareTo(b) <= 0 && a.compareTo(interval[1]) <= 0) {
          interval[0] = interval[0].min(a);
          interval[1] = interval[1].max(b);
          
          M.set(i, interval);
          return M;
        }
      }
      
      BigInteger[] new_interval = new BigInteger[2];
      new_interval[0] = a;
      new_interval[1] = b;
      
      M.add(new_interval);
      return M;
      
    }
    
    Boolean debug_mode;
    
    @Override
    public BigInteger run(final I_RSAPKCS_OWCL_Challenger challenger) {
        // Write code here!
        //return BigInteger.ZERO;
        Boolean debugging = false;
        this.debug_mode = debugging;
        
        this.challenger_ = challenger;
        
        RSAPKCS_PK pubkey = challenger.getPk();
        BigInteger N = pubkey.N;
        BigInteger e = pubkey.exponent;
        BigInteger ciphertext_BINT = challenger.getChallenge();
        String ciphertext_string = ciphertext_BINT.toString(2);
        if (debugging) {
          System.out.println(ciphertext_BINT);
          System.out.println(ciphertext_string);
        }
        
        this.query_counter = 0;
        
        this.max_queryQuota = (long) 1e7;
        
        int k = (N.bitLength() / 8) + 1; //byte length of N, round up
        //int k = challenger.getPlainTextLength(); //byte length, actually use modulus
        
        //int counter = challenger.getQueryCounter();
        BigInteger TWO = BigInteger.valueOf(2);
        BigInteger THREE = BigInteger.valueOf(3);

        BigInteger B = TWO.pow(8 * (k - 2));
        
        BigInteger TWO_B = B.multiply(TWO);
        BigInteger THREE_B = B.multiply(THREE);
        
        ArrayList<BigInteger[]> M = new ArrayList<BigInteger[]>(); 
        
        
        
        //borders of M, init
        //BigInteger left = TWO_B;
        //BigInteger right = THREE_B.subtract(BigInteger.ONE);
        
        BigInteger[] list = new BigInteger[2];
        list[0] = TWO_B;
        list[1] = THREE_B.subtract(BigInteger.ONE);;
        
        M.add(list); //INIT M
        
        //BigInteger new_left = left;
        //BigInteger new_right = right;
        
        BigInteger c = ciphertext_BINT;
        BigInteger s = BigInteger.ONE;
        
        BigInteger temp;
        
        
        
        for (long i = 1; this.query_counter < this.max_queryQuota; ++i) {
          
          if (debugging) {
            System.out.print("run loop: ");
            System.out.println(i);
          }
          
          if (i == 1) { //2a - CHECKED
          
            if (debugging) {
              System.out.println("Case 2a");
            }
            
            s = N.divide(THREE_B);
            do {
              s = s.add(BigInteger.ONE);
              temp = s.modPow(e, N);
              temp = temp.multiply(c).mod(N);
            } while(!oracle(temp));
            
          }
          else {
            
            if (M.size() >= 2) {//2b
              
              if (debugging) {
                System.out.println("Case 2b");
              }
              
              do {
                s = s.add(BigInteger.ONE);
                temp = s.modPow(e, N);
                temp = temp.multiply(c).mod(N);
              } while(!oracle(temp));
              
            }
            else if (M.size() == 1) { //2c
            
              if (debugging) {
                System.out.println("Case 2c");
              }
              
              //Iterator<BigInteger[]> M_iterator = M.iterator(); 
              BigInteger [] only_M = M.get(0);//.next();
              BigInteger a = only_M[0];
              BigInteger b = only_M[1];
              
              if (a.equals(b)) {
                if (debugging) {
                  System.out.println("Case 4 - SOLVED");
                }
                this.m = a.mod(N);
                break;
              }
              
              BigInteger bottom_r = b.multiply(s).subtract(TWO_B);
              bottom_r = bottom_r.multiply(TWO).divide(N);
              bottom_r = bottom_r.add(BigInteger.ONE);
              
              
              Boolean found_s_flag = false;
            
              for (BigInteger r = bottom_r; !found_s_flag; r = r.add(BigInteger.ONE)) {
                BigInteger rn = r.multiply(N);
                BigInteger bottom = TWO_B.add(rn);
                bottom = bottom.divide(b);
                //bottom = bottom.add(BigInteger.ONE);
                
                BigInteger top = THREE_B.add(rn);
                top = top.divide(a);
                top = top.add(BigInteger.ONE);
                
                for (s = bottom; s.compareTo(top) < 0; s = s.add(BigInteger.ONE)) {
                  temp = s.modPow(e, N);
                  temp = temp.multiply(c).mod(N);
                  if (oracle(temp)) {
                    found_s_flag = true;
                    break;
                  }  
                }
              }
              
              
            } //M.size() == 1
            
          } //i > 2 else
          
          //3
          if (debugging) {
            System.out.println("Case 3");
          }
          
          //Iterator<BigInteger[]> M_iterator = M.iterator();
          ArrayList<BigInteger[]> new_M = new ArrayList<BigInteger[]>(); 
          
          //while (M_iterator.hasNext()) {
          for (int ith_interval = 0; ith_interval < M.size(); ith_interval++) {
            
            BigInteger[] temp_a_b_list = M.get(ith_interval);
            BigInteger a = temp_a_b_list[0];
            BigInteger b = temp_a_b_list[1];
            
            BigInteger bottom = a.multiply(s);
            bottom = bottom.subtract(THREE_B).add(BigInteger.ONE);
            bottom = bottom.divide(N);
            //bottom = bottom.add(BigInteger.ONE);
                          
            BigInteger top = b.multiply(s);
            top = top.subtract(TWO_B);
            top = top.divide(N);
            top = top.add(BigInteger.ONE);
            
            for (BigInteger r = bottom; r.compareTo(top) < 0; r = r.add(BigInteger.ONE)) {
              
              BigInteger[] new_temp_list = new BigInteger[2];
              
              BigInteger rn = r.multiply(N);
              BigInteger temp_ = TWO_B.add(rn);
              temp_ = temp_.divide(s);
              temp_ = temp_.add(BigInteger.ONE);
              
              new_temp_list[0] = a.max(temp_);
              
              temp_ = THREE_B.add(rn).subtract(BigInteger.ONE);
              temp_ = temp_.divide(s);
              
              new_temp_list[1] = b.min(temp_);
              
              if (new_temp_list[0].compareTo(new_temp_list[1]) <= 0) {
                new_M = check_overlap(new_M, new_temp_list[0], new_temp_list[1]);
              }
              
              //new_M = union(new_M, new_temp_list[0], new_temp_list[1]);
              
              //new_M.add(new_temp_list);
              
              //add_to_M(new_M, new_temp_list[0], new_temp_list[1]);
            }
          }
          M = new_M;
          
          if (debugging) {
            System.out.print("M size: ");
            System.out.println(M.size());
            System.out.println("*********");
            if (M.size()  == 1) {
              System.out.print("[ ");
              System.out.print(M.get(0)[0]);
              System.out.print(" , ");
              System.out.print(M.get(0)[1]);
              System.out.println(" ]");
              System.out.print("Diff: ");
              System.out.println(M.get(0)[1].subtract(M.get(0)[0]));
            }
            else if(M.size() == 2) {
              System.out.print("[ ");
              System.out.print(M.get(0)[0]);
              System.out.print(" , ");
              System.out.print(M.get(0)[1]);
              System.out.println(" ]");
              System.out.print("Diff: ");
              System.out.println(M.get(0)[1].subtract(M.get(0)[0]));
              
              System.out.print("[ ");
              System.out.print(M.get(1)[0]);
              System.out.print(" , ");
              System.out.print(M.get(1)[1]);
              System.out.println(" ]");
              System.out.print("Diff: ");
              System.out.println(M.get(1)[1].subtract(M.get(1)[0]));
              
            }
            else {
              System.out.println("Multiple intervals present");
            }
//            System.out.print("[ ");
//            System.out.print(M.get(0)[0]);
//            System.out.print(" , ");
//            System.out.print(M.get(0)[1]);
//            System.out.println(" ]");
//            for(int kk = 0; k < M.size(); ++kk) {
//              BigInteger[] printing_interval = M.get(kk);
//              System.out.print("[ ");
//              System.out.print(printing_interval[0]);
//              System.out.print(" , ");
//              System.out.print(printing_interval[1]);
//              System.out.println(" ]");
//              //System.out.println(Arrays.toString(M.get(kk)));
//            }
            System.out.println("*********");
          }
          
          // if (debugging) {
          //   System.out.println("Case 4");
          // }
          // if (M.size() == 1) { //4
          //   Iterator<BigInteger[]> M_iterator_temp = M.iterator(); 
          //   BigInteger[] interval = M_iterator_temp.next();
          //   if (interval[0].equals(interval[1])) {
          //     this.m = interval[0].mod(N);
          //     break;
          //   }
          // }
          
        }
        
        
        
        int plength = challenger.getPlainTextLength() * 8; //in bitlength
        
        String bit_plaintext = this.m.toString(2);
        //System.out.println(plaintext);
        bit_plaintext = bit_plaintext.substring(bit_plaintext.length() - plength); //take last bits -> get message
        
        if (debugging) {
          BigInteger cipher = this.m.modPow(e, N);
          Boolean correctness = cipher.equals(c);
          System.out.print("Correct?: ");
          System.out.println(correctness);
          System.out.print("Bit plaintext: ");
          System.out.println(bit_plaintext);
        }

        BigInteger solution = new BigInteger(bit_plaintext, 2);
        //return this.m;
        return solution;
        
    }
}