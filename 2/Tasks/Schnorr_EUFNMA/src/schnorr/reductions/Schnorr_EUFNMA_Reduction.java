package schnorr.reductions;

import java.math.BigInteger;
import java.util.Random;

import dlog.I_DLog_Challenger;
import genericGroups.IGroupElement;
import schnorr.I_Schnorr_EUFNMA_Adversary;
import schnorr.Schnorr_PK;
import utils.NumberUtils;
import utils.Pair;
import utils.StringUtils;
import utils.Triple;

public class Schnorr_EUFNMA_Reduction extends A_Schnorr_EUFNMA_Reduction {

    public Schnorr_EUFNMA_Reduction(I_Schnorr_EUFNMA_Adversary<IGroupElement, BigInteger> adversary) {
        super(adversary);
        // Do not change this constructor!
    }

    @Override
    public Schnorr_PK<IGroupElement> getChallenge() {
        // Write your Code here!
        return null;
    }

    @Override
    public BigInteger hash(String message, IGroupElement r) {
        // Write your Code here!
        return null;
    }

    @Override
    public BigInteger run(I_DLog_Challenger<IGroupElement> challenger) {
        // Write your Code here!

        // You can use all classes and methods from the util package:
        var randomNumber = NumberUtils.getRandomBigInteger(new Random(),
                challenger.getChallenge().generator.getGroupOrder());
        var randomString = StringUtils.generateRandomString(new Random(), 10);
        var pair = new Pair<Integer, Integer>(5, 8);
        var triple = new Triple<Integer, Integer, Integer>(13, 21, 34);

        return null;
    }

}
