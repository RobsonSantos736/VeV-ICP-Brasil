import java.io.*;
import java.security.*;
import java.security.spec.*;
import java.util.Base64;

public class KATTestBouncyCastleExtended {
    public static void main(String[] args) throws Exception {
        String msg = "Mensagem de teste ICP-Brasil";
        byte[] dados = msg.getBytes();

        // ===== RSA/SHA-256 =====
        System.out.println("\n=== TESTE RSA/SHA-256 ===");
        KeyFactory kfRSA = KeyFactory.getInstance("RSA");
        PrivateKey privRSA = kfRSA.generatePrivate(new PKCS8EncodedKeySpec(
                java.nio.file.Files.readAllBytes(new File("keys/chave_privada_rsa.der").toPath())));
        PublicKey pubRSA = kfRSA.generatePublic(new X509EncodedKeySpec(
                java.nio.file.Files.readAllBytes(new File("keys/chave_publica_rsa.der").toPath())));

        Signature sigRSA = Signature.getInstance("SHA256withRSA");
        sigRSA.initSign(privRSA);
        sigRSA.update(dados);
        byte[] assinaturaRSA = sigRSA.sign();
        System.out.println("Assinatura RSA: " + Base64.getEncoder().encodeToString(assinaturaRSA));

        sigRSA.initVerify(pubRSA);
        sigRSA.update(dados);
        System.out.println("Resultado RSA: " + (sigRSA.verify(assinaturaRSA) ? "✅ PASS" : "❌ FAIL"));

        // ===== ECDSA/SHA-512 =====
        System.out.println("\n=== TESTE ECDSA/SHA-512 ===");
        KeyFactory kfEC = KeyFactory.getInstance("EC");
        PrivateKey privEC = kfEC.generatePrivate(new PKCS8EncodedKeySpec(
                java.nio.file.Files.readAllBytes(new File("keys/chave_privada_ecdsa.der").toPath())));
        PublicKey pubEC = kfEC.generatePublic(new X509EncodedKeySpec(
                java.nio.file.Files.readAllBytes(new File("keys/chave_publica_ecdsa.der").toPath())));

        Signature sigEC = Signature.getInstance("SHA512withECDSA");
        sigEC.initSign(privEC);
        sigEC.update(dados);
        byte[] assinaturaEC = sigEC.sign();
        System.out.println("Assinatura ECDSA: " + Base64.getEncoder().encodeToString(assinaturaEC));

        sigEC.initVerify(pubEC);
        sigEC.update(dados);
        System.out.println("Resultado ECDSA: " + (sigEC.verify(assinaturaEC) ? "✅ PASS" : "❌ FAIL"));
    }
}
