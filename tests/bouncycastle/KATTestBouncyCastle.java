import java.io.*;
import java.security.*;
import java.security.spec.*;
import java.util.Base64;

public class KATTestBouncyCastle {
    public static void main(String[] args) throws Exception {
        String mensagem = "Mensagem de teste ICP-Brasil";

        // Carregar chaves RSA (PKCS#8 e X.509)
        byte[] privKeyBytes = java.nio.file.Files.readAllBytes(new File("chave_privada.der").toPath());
        byte[] pubKeyBytes  = java.nio.file.Files.readAllBytes(new File("chave_publica.der").toPath());

        KeyFactory kf = KeyFactory.getInstance("RSA");
        PrivateKey privateKey = kf.generatePrivate(new PKCS8EncodedKeySpec(privKeyBytes));
        PublicKey publicKey   = kf.generatePublic(new X509EncodedKeySpec(pubKeyBytes));

        // Gerar hash e assinatura
        Signature signature = Signature.getInstance("SHA256withRSA");
        signature.initSign(privateKey);
        signature.update(mensagem.getBytes());
        byte[] assinatura = signature.sign();
        System.out.println("Assinatura (Base64): " + Base64.getEncoder().encodeToString(assinatura));

        // Verificar assinatura
        signature.initVerify(publicKey);
        signature.update(mensagem.getBytes());
        boolean resultado = signature.verify(assinatura);

        if (resultado)
            System.out.println("Resultado: ✅ PASS - Assinatura válida");
        else
            System.out.println("Resultado: ❌ FAIL - Assinatura inválida");
    }
}
