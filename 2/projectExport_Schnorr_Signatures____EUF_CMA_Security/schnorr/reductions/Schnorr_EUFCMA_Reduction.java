package schnorr.reductions;

import java.math.BigInteger;
import java.security.SecureRandom;
import java.util.HashMap;
import java.util.Random;

import dlog.DLog_Challenge;
import dlog.I_DLog_Challenger;
import genericGroups.IGroupElement;
import schnorr.I_Schnorr_EUFCMA_Adversary;
import schnorr.SchnorrSignature;
import schnorr.SchnorrSolution;
import schnorr.Schnorr_PK;
import utils.NumberUtils;
import utils.Pair;


import java.util.*;
import dlog.*;
import schnorr.SchnorrSolution;
import schnorr.SchnorrSignature;
import schnorr.Schnorr_PK;

import java.security.SecureRandom;


public class Schnorr_EUFCMA_Reduction extends A_Schnorr_EUFCMA_Reduction {

    public Schnorr_EUFCMA_Reduction(I_Schnorr_EUFCMA_Adversary<IGroupElement, BigInteger> adversary) {
        super(adversary);
        // Do not change this constructor!
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
    
    public Hashtable<Pair<String, IGroupElement>, BigInteger> hash_hashmap;
    public Hashtable<String, SchnorrSignature<BigInteger>> sign_hashmap;
  
    public Random RNG;
    public BigInteger p;
    public Boolean debugging;
    
    public void setup(DLog_Challenge<IGroupElement> challenge) { //checked
      this.p = challenge.generator.getGroupOrder();
      this.pubkey = challenge.x;
      this.generator = challenge.generator;
      this.RNG = new Random();
      this.hash_hashmap = new Hashtable<Pair<String, IGroupElement>, BigInteger>();
      this.sign_hashmap = new Hashtable<String, SchnorrSignature<BigInteger>>();
      
      this.debugging = false;
    }

    @Override
    public Schnorr_PK<IGroupElement> getChallenge() {
        // Implement your code here!
        IGroupElement generator = this.generator;
        IGroupElement pubkey = this.pubkey;
        Schnorr_PK<IGroupElement> schnorr_pk = new Schnorr_PK<IGroupElement>(generator, pubkey);
        return schnorr_pk;
    }

    @Override
    public SchnorrSignature<BigInteger> sign(String message) {
        // Implement your code here!
        //return null;
        
        if (this.debugging) {
          System.out.print("Sign for message: ");
          System.out.println(message);
        }
        
        BigInteger c;
        BigInteger s;
        IGroupElement gs;
        IGroupElement pubkey_inv;
        IGroupElement pubkey_minus_c;
        IGroupElement r;
        Boolean hashmap_already_contains_value;
        Pair<String, IGroupElement> element;
        
        do {
          c = getRandomBigInteger(this.RNG, this.p);
          s = getRandomBigInteger(this.RNG, this.p);
          gs = this.generator.power(s);
          pubkey_inv = this.pubkey.invert();
          pubkey_minus_c = pubkey_inv.power(c);
          r = gs.multiply(pubkey_minus_c);
          element = new Pair<String, IGroupElement>(message, r);
          hashmap_already_contains_value = this.hash_hashmap.containsKey(message) && !c.equals(this.hash_hashmap.get(message));
        } while(hashmap_already_contains_value);
        
        hash_hashmap.put(element, c);
        SchnorrSignature<BigInteger> signature = new SchnorrSignature<BigInteger>(c, s);
        sign_hashmap.put(message, signature);
        return signature;
      
    }

    @Override
    public BigInteger hash(String message, IGroupElement r) {
        // Implement your code here!
        
        if (this.debugging) {
          System.out.print("Hash for message: ");
          System.out.print(message);
          System.out.print(" ; ele = ");
          System.out.println(r.toString().substring(27));
        }
        
        if (this.sign_hashmap.containsKey(message)) {
          SchnorrSignature<BigInteger> signature = this.sign_hashmap.get(message);
          BigInteger c = signature.c;
          return c;
          
          // BigInteger s = signature.s;
          // IGroupElement gs = this.generator.power(s);
          // IGroupElement pubkey_inv = this.pubkey.invert();
          // IGroupElement pubkey_minus_c = pubkey_inv.power(c);
          // IGroupElement r_stored = gs.multiply(pubkey_minus_c);
          
          // if (r.equals(r_stored)) {
          //   return c;
          // }
          // else {
          //   System.out.println("Not equal!");
          // }
        }
        
        var element = new Pair<String, IGroupElement>(message, r);
        BigInteger ret_value;
        if (this.hash_hashmap.containsKey(element)) {
          ret_value =  this.hash_hashmap.get(element);
        }
        else {
          BigInteger value = getRandomBigInteger(this.RNG, this.p);
          hash_hashmap.put(element, value);
          ret_value = value;
        }
        return ret_value;
    }
    
    public void rewind_hashmap(SchnorrSolution<BigInteger> forgery) {
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
      
      this.hash_hashmap.clear();
      this.sign_hashmap.clear();
      
      hash_hashmap.put(element, new_c); //forking
    }

    @Override
    public BigInteger run(I_DLog_Challenger<IGroupElement> challenger) {
        // Implement your code here!
        DLog_Challenge<IGroupElement> challenge = challenger.getChallenge();
        setup(challenge);
        adversary.reset(0);
        SchnorrSolution<BigInteger> forgery1 = adversary.run(this);
        
        
        // System.out.print("forgery1 = ");
        // System.out.println(forgery1);
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
          
          BigInteger ret_value = this.hash_hashmap.get(element);
          System.out.print("Correctness 1: ");
          System.out.println(c1.equals(ret_value));
        }
        
        
        rewind_hashmap(forgery1);
 
        adversary.reset(0);
        SchnorrSolution<BigInteger> forgery2 = adversary.run(this);
        
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
          
          BigInteger ret_value = this.hash_hashmap.get(element);
          System.out.print("Correctness 2: ");
          System.out.println(c2.equals(ret_value));
        }
        
        BigInteger s_diff = s1.subtract(s2);
        BigInteger c_diff = c1.subtract(c2);
        
        BigInteger c_diff_inv = c_diff.modInverse(this.p);
        // BigInteger s_diff_inv = s_diff.modInverse(this.p);
        
        BigInteger temp  = s_diff.multiply(c_diff_inv);
        BigInteger solution = temp.mod(this.p);
        
        Boolean iscorrect = challenger.checkSolution(solution);
        if (this.debugging) {
          System.out.print("Answer: ");
          System.out.println(iscorrect);
          System.out.println("");
        }
        
        return solution;
    }
}
