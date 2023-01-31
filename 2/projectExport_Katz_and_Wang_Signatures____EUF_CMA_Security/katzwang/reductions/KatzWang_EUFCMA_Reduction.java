package katzwang.reductions;

import java.math.BigInteger;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

import ddh.DDH_Challenge;
import ddh.I_DDH_Challenger;
import genericGroups.IGroupElement;
import katzwang.A_KatzWang_EUFCMA_Adversary;
import katzwang.KatzWangPK;
import katzwang.KatzWangSignature;
import katzwang.KatzWangSolution;
import utils.NumberUtils;
import utils.Triple;


import java.util.*;
import katzwang.KatzWangSignature;
import katzwang.KatzWangSolution;
import ddh.DDH_Challenge;
import java.security.SecureRandom;


public class KatzWang_EUFCMA_Reduction extends A_KatzWang_EUFCMA_Reduction {

    public KatzWang_EUFCMA_Reduction(A_KatzWang_EUFCMA_Adversary adversary) {
        super(adversary);
        // Do not change this constructor
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
    
    public IGroupElement generator;
    public IGroupElement x;
    public IGroupElement y;
    public IGroupElement z;
    
    public BigInteger p;
    public IGroupElement e; 
    public Random RNG;
    
    
    public Hashtable<Triple<IGroupElement, IGroupElement, String>, BigInteger> hash_hashtable;
    public Hashtable<String, KatzWangSignature<BigInteger>> sign_hashtable;
    
    //public Boolean bad_rom_request;
    public Boolean debugging;
    
    public void setup(DDH_Challenge<IGroupElement> challenge) {
      this.generator = challenge.generator;
      this.x = challenge.x;
      this.y = challenge.y;
      this.z = challenge.z;
      this.p = challenge.generator.getGroupOrder();
      this.e = challenge.generator.power(BigInteger.ZERO);
      this.RNG = new Random();
      this.hash_hashtable = new Hashtable<Triple<IGroupElement, IGroupElement, String>, BigInteger>();
      this.sign_hashtable = new Hashtable<String, KatzWangSignature<BigInteger>>();
      //this.bad_rom_request = false;
      
      this.debugging = false;
    }

    @Override
    public Boolean run(I_DDH_Challenger<IGroupElement, BigInteger> challenger) {
        // Implement your code here!
        DDH_Challenge<IGroupElement> challenge = challenger.getChallenge();
        //System.out.println(challenge); //not null
        setup(challenge);
        KatzWangSolution<BigInteger> forgery = adversary.run(this); //null -> not real
        if (forgery == null) {
          if (this.debugging) {
            System.out.print("Forgery: ");
            System.out.println(forgery);
          }
          return false;
        }
        if (this.debugging) {
          System.out.println(forgery);
        }
        String forged_message = forgery.message;
        KatzWangSignature<BigInteger> signature = forgery.signature;
        BigInteger s = signature.s;
        BigInteger c = signature.c;
        
        IGroupElement g_s = this.generator.power(s);
        IGroupElement h_s = this.x.power(s);
        IGroupElement y1_c = this.y.power(c);
        IGroupElement y2_c = this.z.power(c);
        IGroupElement y1_minus_c = y1_c.invert();
        IGroupElement y2_minus_c = y2_c.invert();
        
        IGroupElement A = g_s.multiply(y1_minus_c);
        IGroupElement B = h_s.multiply(y2_minus_c);
        
        var element = new Triple<IGroupElement, IGroupElement, String>(A, B, forged_message);
        if (this.hash_hashtable.containsKey(element)) {
          BigInteger c_from_rom = this.hash_hashtable.get(element);
          if (c.equals(c_from_rom)) {
            return true;
          }
          else {
            return false;
          }
        }
        return false;
        //return false;
    }

    @Override
    public KatzWangPK<IGroupElement> getChallenge() {
        // Implement your code here!
        //BigInteger a = getRandomBigInteger(this.RNG, this.p);
        //BigInteger b = getRandomBigInteger(this.RNG, this.p);
        //KatzWangPK<IGroupElement> pubkey = new KatzWangPK<IGroupElement>(this.generator, this.generator.power(a), this.generator.power(b), this.generator.power(a).power(b));
        KatzWangPK<IGroupElement> pubkey = new KatzWangPK<IGroupElement>(this.generator, this.x, this.y, this.z);
        return pubkey;
    }

    @Override
    public BigInteger hash(IGroupElement comm1, IGroupElement comm2, String message) {
        // Implement your code here!
        
        if (this.debugging) {
          System.out.print("Message: ");
          System.out.println(message);
        }
        
        
        if (this.sign_hashtable.containsKey(message)) {
          KatzWangSignature<BigInteger> signature = this.sign_hashtable.get(message);
          BigInteger c = signature.c;
          return c;
        }
        
        var element = new Triple<IGroupElement, IGroupElement, String>(comm1, comm2, message);
        BigInteger c;
        if (this.hash_hashtable.containsKey(element)) {
          //BigInteger rand_c = getRandomBigInteger(this.RNG, this.p);
          //return BigInteger.ZERO.subtract(rand_c);
          //c = BigInteger.MinusOne;
          //this.bad_rom_request = true;
          c = this.hash_hashtable.get(element);
        }
        else {
          BigInteger rand_c = getRandomBigInteger(this.RNG, this.p);
          this.hash_hashtable.put(element, rand_c);
          c = rand_c;
        }
        return c;
    }

    @Override
    public KatzWangSignature<BigInteger> sign(String message) {
        // Implement your code here!
        
        if (this.debugging) {
          System.out.print("Sign for message: ");
          System.out.println(message);
        }
        
        BigInteger c;
        BigInteger s;
        IGroupElement g_s;
        IGroupElement h_s;
        IGroupElement y1_c;
        IGroupElement y2_c;
        IGroupElement y1_minus_c;
        IGroupElement y2_minus_c;
        IGroupElement A;
        IGroupElement B; 
        Triple<IGroupElement, IGroupElement, String> element;
        Boolean hashtable_already_contains_value;
        
        do {
          c = getRandomBigInteger(this.RNG, this.p);
          s = getRandomBigInteger(this.RNG, this.p);
          g_s = this.generator.power(s);
          h_s = this.x.power(s);
          y1_c = this.y.power(c);
          y2_c = this.z.power(c);
          y1_minus_c = y1_c.invert();
          y2_minus_c = y2_c.invert();
          
          A = g_s.multiply(y1_minus_c);
          B = h_s.multiply(y2_minus_c);
          element = new Triple<IGroupElement, IGroupElement, String>(A, B, message);
          hashtable_already_contains_value = this.hash_hashtable.containsKey(element) && !c.equals(this.hash_hashtable.get(element));
          //if true then this.bad_rom_request = true; -> preventable with loop
          
        } while(hashtable_already_contains_value);
        
        hash_hashtable.put(element, c);
        KatzWangSignature<BigInteger> signature = new KatzWangSignature<BigInteger>(c, s);
        
        sign_hashtable.put(message, signature);
        return signature;
    }
}
