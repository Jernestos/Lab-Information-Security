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
import dlog.I_DLog_Adversary;

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
		
		public Hashtable<Pair<String, IGroupElement>, BigInteger> hashtable;
		public Random RNG;
		public BigInteger p;
		
		public HashSet<String> hashset;
		
		//debugging
		public List<String> msg_history;
		public List<IGroupElement> element_history;
		public Boolean printing; //debugging
		
		public void setup(DLog_Challenge<IGroupElement> challenge) { //checked
			this.p = challenge.generator.getGroupOrder();
			this.pubkey = challenge.x;
			this.generator = challenge.generator;
			this.RNG = new Random();
			this.hashtable = new Hashtable<Pair<String, IGroupElement>, BigInteger>();
			this.hashset = new HashSet<String>();
			//works
			// System.out.println(this.p);
			// System.out.println(this.pubkey);
			// System.out.println(this.generator);
			// System.out.println(this.RNG);
			// System.out.println(this.hashtable);
			//debugging
			this.msg_history = new ArrayList<String>();
			this.element_history = new ArrayList<IGroupElement>();
			this.printing = true; //debugging
		}

		@Override
		public Schnorr_PK<IGroupElement> getChallenge() {
				// Implement your code here!
				IGroupElement generator = this.generator;
				IGroupElement pubkey = this.pubkey;
				Schnorr_PK<IGroupElement> schnorr_pk = new Schnorr_PK<IGroupElement>(generator, pubkey);
				// System.out.print("Printing out pk: ");
				// System.out.println(schnorr_pk); //not null
				if (this.printing) {
					System.out.println("Init adv.");
				}
				return schnorr_pk;
		}

		@Override
		public SchnorrSignature<BigInteger> sign(String message) {
				// Implement your code here!
				if (this.printing) {
					System.out.print("sign for msg = ");
					System.out.print(message);
					System.out.print(" and r_ele = ");
				}
				
				BigInteger c = getRandomBigInteger(this.RNG, this.p);
				BigInteger s = getRandomBigInteger(this.RNG, this.p);
				IGroupElement g_s = this.generator.power(s);
				IGroupElement temp_pubkey_c = this.pubkey.power(c);
				IGroupElement pubkey_minus_c = temp_pubkey_c.invert();
				IGroupElement r = g_s.multiply(pubkey_minus_c);
				
				if (this.printing) {
					System.out.println(r.toString().substring(26));
				}
				
				//BigInteger def_c = hash(message, r);
				//c = def_c;
				
				var element = new Pair<String, IGroupElement>(message, r);
				BigInteger ret_value;
				if (this.hashtable.containsKey(element)) {
					c = this.hashtable.get(element); //uar c value so it's okay
				}
				else {
					hashtable.put(element, c);
				}
				
				// this.msg_history.add(message);
				// this.element_history.add(r);
				
				SchnorrSignature<BigInteger> signature = new SchnorrSignature<BigInteger>(c, s);
				return signature;
				
				
				// BigInteger c;
				// BigInteger s;
				// IGroupElement g_s;
				// IGroupElement temp_pubkey_c;
				// IGroupElement pubkey_minus_c;
				// IGroupElement r;
				// Pair<String, IGroupElement> element;
				// Boolean condition;
				
				// do {
				//   c = getRandomBigInteger(this.RNG, this.p);
				//   s = getRandomBigInteger(this.RNG, this.p);
					
				//   g_s = this.generator.power(s);
				//   temp_pubkey_c = this.pubkey.power(c);
				//   pubkey_minus_c = temp_pubkey_c.invert();
				//   r = g_s.multiply(pubkey_minus_c);
				//   element = new Pair<String, IGroupElement>(message, r);
				//   condition = this.hashtable.containsKey(element) && !c.equals(this.hashtable.get(element));
				// } while(condition);
				
				// //condition is false; so either no such mapping exists; or it already maps element to c; either way putting it (again)
				// //into the hashtable does not invalide code
				// hashtable.put(element, c); //check
				// hashset.add(message);
				
				// SchnorrSignature<BigInteger> signature = new SchnorrSignature<BigInteger>(c, s);
				// return signature;
		}

		@Override
		public BigInteger hash(String message, IGroupElement r) { //ROM
				// Implement your code here!
				if (this.printing) {
					System.out.print("hash for msg = ");
					System.out.print(message);
					System.out.print(" and ele = ");
					System.out.println(r.toString().substring(26));
				}
				var element = new Pair<String, IGroupElement>(message, r);
				
				// this.msg_history.add(message);
				// this.element_history.add(r);
				
				BigInteger ret_value;
				if (this.hashtable.containsKey(element)) {
					ret_value = this.hashtable.get(element);
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
			
			//this.hashtable.clear();
			
			hashtable.put(element, new_c); //forking
		}
		
		public void debug_analytics() {
			IGroupElement first_ele = element_history.get(0);
			IGroupElement second_ele = element_history.get(2);
			
			Boolean test = first_ele.equals(second_ele);
			System.out.print("Test: ");
			System.out.println(test);
		}
		
		public BigInteger solve() {
			long magic_number = 0;
			adversary.reset(magic_number);
			SchnorrSolution<BigInteger> forgery1 = adversary.run(this);

			// adversary.reset(magic_number);
			// SchnorrSolution<BigInteger> forgery1 = adversary.run(this); //returns null
			if (forgery1 == null) {
				//debug_analytics();
				
				System.out.print("forgery1 is: ");
				System.out.println(forgery1); //null
			
				return BigInteger.ZERO;  
			}
			SchnorrSignature<BigInteger> sign1 = forgery1.signature;
			BigInteger c1 = sign1.c;
			BigInteger s1 = sign1.s;
			rewind_hashtable(forgery1);
			
			adversary.reset(magic_number);
			SchnorrSolution<BigInteger> forgery2 = adversary.run(this);
			if (forgery2 == null) {
				System.out.print("forgery2 is: ");
				System.out.println(forgery2); //null
				return BigInteger.ZERO;  
			}
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

		@Override
		public BigInteger run(I_DLog_Challenger<IGroupElement> challenger) {
				// Implement your code here!
				DLog_Challenge<IGroupElement> challenge = challenger.getChallenge();
				//System.out.println(challenger); not null
				//System.out.println(challenge); //not null
				setup(challenge); //success
				BigInteger solution = solve();
				
				return solution;
				//return null;
		}
}
