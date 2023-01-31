package schnorr.reductions;

import java.math.BigInteger;

import dlog.I_DLog_Challenger;
import genericGroups.IGroupElement;
import schnorr.I_Schnorr_EUFNMA_Adversary;
import schnorr.Schnorr_PK;
import utils.Pair;

import java.util.*;
import dlog.*;
import schnorr.SchnorrSolution;
import schnorr.SchnorrSignature;
import schnorr.Schnorr_PK;

import java.security.SecureRandom;

public class Schnorr_EUFNMA_Reduction extends A_Schnorr_EUFNMA_Reduction{

    public Schnorr_EUFNMA_Reduction(I_Schnorr_EUFNMA_Adversary<IGroupElement, BigInteger> adversary) {
        super(adversary);
        //Do not change this constructor!
    }
    
    public BigInteger getRandomBigInteger(Random RNG, BigInteger max) {
        if (max == null)
            return null;
        if (max.signum() <= 0)
            return null;
        var next = new BigInteger(max.bitLength(), RNG);
        while (next.compareTo(max) >= 0)
            next = new BigInteger(max.bitLength(), RNG);
        return next;
    }
    
    public IGroupElement pubkey;
    public IGroupElement generator;
    
    public Hashtable<Pair<String, IGroupElement>, BigInteger> hashtable;
    public Random RNG;
    public BigInteger p;
    
    public Boolean debugging;
    
    
    public void setup(DLog_Challenge<IGroupElement> challenge) { //checked
      this.p = challenge.generator.getGroupOrder();
      this.pubkey = challenge.x;
      this.generator = challenge.generator;
      this.RNG = new Random();
      this.hashtable = new Hashtable<Pair<String, IGroupElement>, BigInteger>();
    
      this.debugging = false;
    }
    
    @Override
    public Schnorr_PK<IGroupElement> getChallenge() { //checked
        //Write your Code here!
        //return null;
        IGroupElement generator = this.generator;
        IGroupElement pubkey = this.pubkey;
        Schnorr_PK<IGroupElement> schnorr_pk = new Schnorr_PK<IGroupElement>(generator, pubkey);
        return schnorr_pk;
    }

    @Override
    public BigInteger hash(String message, IGroupElement r) { //checked
        //Write your Code here!
        //return null;
        var element = new Pair<String, IGroupElement>(message, r);
        BigInteger ret_value;
        if (this.hashtable.containsKey(element)) {
          ret_value =  this.hashtable.get(element);
        }
        else {
          BigInteger value = getRandomBigInteger(this.RNG, this.p);
          hashtable.put(element, value);
          ret_value = value;
        }
        return ret_value;
    }
    
    public void rewind_hashtable(SchnorrSolution<BigInteger> forgery) {
      String message = forgery.message;
      SchnorrSignature<BigInteger> sign = forgery.signature;
      BigInteger c = sign.c;
      BigInteger s = sign.s;
      
      IGroupElement g_s = this.generator.power(s);
      
      IGroupElement temp_pubkey_c = this.pubkey.power(c);
      IGroupElement pubkey_minus_c = temp_pubkey_c.invert();
      IGroupElement r = g_s.multiply(pubkey_minus_c);
      
      //IGroupElement pubkey_c = this.pubkey.power(c);
      //IGroupElement r = g_s.multiply(pubkey_c);
      var element = new Pair<String, IGroupElement>(message, r);
      
      BigInteger new_c;
      do {
        new_c = getRandomBigInteger(this.RNG, this.p);
      } while (new_c.equals(c));
      
      this.hashtable.clear();
      
      hashtable.put(element, new_c); //forking
    }
    
    public BigInteger solve() {
      adversary.reset(0);
      SchnorrSolution<BigInteger> forgery1 = adversary.run(this);
      
      SchnorrSignature<BigInteger> sign1 = forgery1.signature;
      BigInteger c1 = sign1.c;
      BigInteger s1 = sign1.s;
      
      rewind_hashtable(forgery1);
      
      adversary.reset(0);
      SchnorrSolution<BigInteger> forgery2 = adversary.run(this);
      
      SchnorrSignature<BigInteger> sign2 = forgery2.signature;
      
      BigInteger c2 = sign2.c;
      BigInteger s2 = sign2.s;
      
      BigInteger s_diff = s1.subtract(s2);
      BigInteger c_diff = c1.subtract(c2);
      
      if (s_diff.compareTo(BigInteger.ZERO) == 0) {
        System.out.println("SAME S");
      }
      
      if (c_diff.compareTo(BigInteger.ZERO) == 0) {
        System.out.println("SAME C");
      }
      
      BigInteger c_diff_inv = c_diff.modInverse(this.p);
      // BigInteger s_diff_inv = s_diff.modInverse(this.p);
      
      BigInteger temp  = s_diff.multiply(c_diff_inv);
      BigInteger exponent = temp.mod(this.p);
      
      return exponent;
    }
    
    public BigInteger solve_() {
      adversary.reset(0);
      SchnorrSolution<BigInteger> forgery1 = adversary.run(this);
      //String forged_message = forgery1.message;
      SchnorrSignature<BigInteger> sign1 = forgery1.signature;
      BigInteger c1 = sign1.c;
      BigInteger s1 = sign1.s;
      
      // IGroupElement g_s = this.generator.power(s1);
      // IGroupElement temp_g_cx = this.pubkey.power(c1);
      // IGroupElement g_minus_cx = temp_g_cx.invert();
      // IGroupElement R = g_s.multiply(g_minus_cx);
      
      // var element = new Pair<String, IGroupElement>(forged_message, R);
      // BigInteger new_c;
      // do {
      //   new_c = getRandomBigInteger(this.RNG, this.p);
      // } while (new_c.equals(c1));
      
      // hashtable.put(element, new_c);
      
      adversary.reset(0);
      SchnorrSolution<BigInteger> forgery2 = adversary.run(this);
      SchnorrSignature<BigInteger> sign2 = forgery2.signature;
      BigInteger c2 = sign2.c;
      BigInteger s2 = sign2.s;
      
      BigInteger s_diff = s1.subtract(s2);
      BigInteger c_diff = c1.subtract(c2);
      
      if (s_diff.compareTo(BigInteger.ZERO) == 0) {
        System.out.println("SAME S");
      }
      
      if (c_diff.compareTo(BigInteger.ZERO) == 0) {
        System.out.println("SAME C");
      }
      
      BigInteger c_diff_inv = c_diff.modInverse(this.p);
      BigInteger s_diff_inv = s_diff.modInverse(this.p);
      
      BigInteger temp  = s_diff.multiply(c_diff_inv);
      BigInteger exponent = temp.mod(this.p);
      return exponent;
    }
    
  
  
    @Override
    public BigInteger run(I_DLog_Challenger<IGroupElement> challenger) {
        //Write your Code here!
        
                // You can use the Triple class...
        //var pair = new Pair<Integer, Integer>(1, 2);
        
        DLog_Challenge<IGroupElement> challenge = challenger.getChallenge();
        setup(challenge);
        
        
        
        
        adversary.reset(0);
        SchnorrSolution<BigInteger> forgery1 = adversary.run(this);
        
        if (this.debugging) {
          System.out.print("forgery1 = ");
          System.out.println(forgery1);
          if (forgery1 == null) {
            return BigInteger.ZERO;  
          }
        }
        
        
        SchnorrSignature<BigInteger> sign1 = forgery1.signature;
        BigInteger c1 = sign1.c;
        BigInteger s1 = sign1.s;
        
        if (this.debugging) {
          IGroupElement g_s = this.generator.power(s1);
      
          IGroupElement temp_pubkey_c = this.pubkey.power(c1);
          IGroupElement pubkey_minus_c = temp_pubkey_c.invert();
          IGroupElement r = g_s.multiply(pubkey_minus_c);
          
          //IGroupElement pubkey_c = this.pubkey.power(c);
          //IGroupElement r = g_s.multiply(pubkey_c);
          var element = new Pair<String, IGroupElement>(forgery1.message, r);
          
          BigInteger ret_value = this.hashtable.get(element);
          System.out.print("Correctness: ");
          System.out.println(c1.equals(ret_value));
        }
        
        rewind_hashtable(forgery1);
        
        adversary.reset(0);
        SchnorrSolution<BigInteger> forgery2 = adversary.run(this);
        
        if (this.debugging) {
          System.out.print("forgery2 = ");
          System.out.println(forgery2);
          if (forgery2 == null) {
            return BigInteger.ZERO;  
          }
        }
        
        SchnorrSignature<BigInteger> sign2 = forgery2.signature;
        
        BigInteger c2 = sign2.c;
        BigInteger s2 = sign2.s;
        
        if (this.debugging) {
          IGroupElement g_s = this.generator.power(s2);
      
          IGroupElement temp_pubkey_c = this.pubkey.power(c2);
          IGroupElement pubkey_minus_c = temp_pubkey_c.invert();
          IGroupElement r = g_s.multiply(pubkey_minus_c);
          
          //IGroupElement pubkey_c = this.pubkey.power(c);
          //IGroupElement r = g_s.multiply(pubkey_c);
          var element = new Pair<String, IGroupElement>(forgery2.message, r);
          
          BigInteger ret_value = this.hashtable.get(element);
          System.out.print("Correctness: ");
          System.out.println(c2.equals(ret_value));
        }
        
        
        BigInteger s_diff = s1.subtract(s2);
        BigInteger c_diff = c1.subtract(c2);
        
        if (s_diff.compareTo(BigInteger.ZERO) == 0) {
          System.out.println("SAME S");
        }
        
        if (c_diff.compareTo(BigInteger.ZERO) == 0) {
          System.out.println("SAME C");
        }
        
        BigInteger c_diff_inv = c_diff.modInverse(this.p);
        // BigInteger s_diff_inv = s_diff.modInverse(this.p);
        
        BigInteger temp  = s_diff.multiply(c_diff_inv);
        BigInteger solution = temp.mod(this.p);
        
        //return exponent;
        
        
        
        
        
        // BigInteger solution = solve();
        
        Boolean iscorrect = challenger.checkSolution(solution);
        if (this.debugging) {
          System.out.print("Answer: ");
          System.out.println(iscorrect);
          System.out.println("");
        }
        //System.out.println(iscorrect);
        return solution;
        
        //return null;
    }
    
}
