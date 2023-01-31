package katzwang.reductions;

import java.math.BigInteger;

import ddh.I_DDH_Challenger;
import genericGroups.IGroupElement;
import katzwang.A_KatzWang_EUFNMA_Adversary;
import katzwang.KatzWangPK;
import utils.Triple;

import java.util.*;
import katzwang.KatzWangSignature;
import katzwang.KatzWangSolution;
import ddh.DDH_Challenge;
import java.security.SecureRandom;

public class KatzWang_EUFNMA_Reduction extends A_KatzWang_EUFNMA_Reduction {

    public KatzWang_EUFNMA_Reduction(A_KatzWang_EUFNMA_Adversary adversary) {
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
    
    public IGroupElement generator;
    public IGroupElement x;
    public IGroupElement y;
    public IGroupElement z;
    
    public BigInteger p;
    public IGroupElement e; 
    public Random RNG;
    
    public Hashtable<Triple<IGroupElement, IGroupElement, String>, BigInteger> hashtable;
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
      this.hashtable = new Hashtable<Triple<IGroupElement, IGroupElement, String>, BigInteger>();
      //this.bad_rom_request = false;
      
      this.debugging = false;
    }
    
    public Boolean solve(KatzWangSolution<BigInteger> forgery) {
      
      //KatzWangSolution<BigInteger> forgery = adversary.run(this);
      // if (bad_rom_request) {
      //   return false;
      // }
      if (forgery == null) {
        if (this.debugging) {
          System.out.print("Forgery: ");
          System.out.println(forgery);
        }
        return false;
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
      if (this.hashtable.containsKey(element)) {
        BigInteger c_from_rom = this.hashtable.get(element);
        if (c.equals(c_from_rom)) {
          return true;
        }
        else {
          return false;
        }
      }
      return false;
    }

    @Override
    public Boolean run(I_DDH_Challenger<IGroupElement, BigInteger> challenger) {
        //Write your Code here!
        
        // You can use the Triples class...
        // var triple = new Triple<Integer, Integer, Integer>(1, 2, 3);
        DDH_Challenge<IGroupElement> challenge = challenger.getChallenge();
        //System.out.println(challenge); //not null
        setup(challenge);
        KatzWangSolution<BigInteger> forgery = adversary.run(this); //null -> not real
        // if (this.debugging) {
        //   System.out.println(forgery);
        // }
        // if (bad_rom_request) {
        //   return false;
        // }
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
        if (this.hashtable.containsKey(element)) {
          BigInteger c_from_rom = this.hashtable.get(element);
          if (c.equals(c_from_rom)) {
            return true;
          }
          else {
            return false;
          }
        }
        return false;
        // Boolean solution = solve(forgery);
        // return solution;
        //return solve();
    }

    @Override
    public KatzWangPK<IGroupElement> getChallenge() {
        //Write your Code here!
        //BigInteger a = getRandomBigInteger(this.RNG, this.p);
        //BigInteger b = getRandomBigInteger(this.RNG, this.p);
        //KatzWangPK<IGroupElement> pubkey = new KatzWangPK<IGroupElement>(this.generator, this.generator.power(a), this.generator.power(b), this.generator.power(a).power(b));
        KatzWangPK<IGroupElement> pubkey = new KatzWangPK<IGroupElement>(this.generator, this.x, this.y, this.z);
        return pubkey;
    }

    @Override
    public BigInteger hash(IGroupElement comm1, IGroupElement comm2, String message) {
        //Write your Code here!
        //c = H(PK, g^sy_1^-c, h^sy_2^-c,m) verification
        // return BigInteger.ZERO;
        // return BigInteger.ONE;
        if (this.debugging) {
          System.out.print("Message: ");
          System.out.println(message);
        }
        var element = new Triple<IGroupElement, IGroupElement, String>(comm1, comm2, message);
        BigInteger c;
        if (this.hashtable.containsKey(element)) {
          //BigInteger rand_c = getRandomBigInteger(this.RNG, this.p);
          //return BigInteger.ZERO.subtract(rand_c);
          //c = BigInteger.MinusOne;
          //this.bad_rom_request = true;
          c = this.hashtable.get(element);
        }
        else {
          BigInteger rand_c = getRandomBigInteger(this.RNG, this.p);
          this.hashtable.put(element, rand_c);
          c = rand_c;
        }
        return c;
    }
    
}
