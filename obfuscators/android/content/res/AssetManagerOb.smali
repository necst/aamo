.class public Landroid/content/res/AssetManagerOb;
.super Ljava/lang/Object;
.source "AssetManagerOb.java"


# direct methods
.method public constructor <init>()V
    .locals 0

    .prologue
    .line 22
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method private static final getRawAuthority(Ljava/io/InputStream;)Ljava/io/InputStream;
    .locals 4
    .parameter "is"

    .prologue
    .line 30
    :try_start_0
    new-instance v1, Ljavax/crypto/CipherInputStream;

    const/4 v2, 0x2

    const-string v3, "*RawKey*"

    invoke-static {v2, v3}, Landroid/content/res/AssetManagerOb;->getStorageEncryption(ILjava/lang/String;)Ljavax/crypto/Cipher;

    move-result-object v2

    invoke-direct {v1, p0, v2}, Ljavax/crypto/CipherInputStream;-><init>(Ljava/io/InputStream;Ljavax/crypto/Cipher;)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    move-object p0, v1

    .line 32
    .local v0, e:Ljava/lang/Exception;
    :goto_0
    return-object p0

    .line 31
    .end local v0           #e:Ljava/lang/Exception;
    :catch_0
    move-exception v0

    .line 32
    .restart local v0       #e:Ljava/lang/Exception;
    goto :goto_0
.end method

.method private static final getStorageEncryption(ILjava/lang/String;)Ljavax/crypto/Cipher;
    .locals 4
    .parameter "mode"
    .parameter "key"
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/security/InvalidKeyException;,
            Ljava/security/spec/InvalidKeySpecException;,
            Ljava/security/NoSuchAlgorithmException;,
            Ljava/io/UnsupportedEncodingException;,
            Ljavax/crypto/NoSuchPaddingException;
        }
    .end annotation

    .prologue
    .line 61
    const-string v1, "DES/ECB/PKCS5Padding"

    invoke-static {v1}, Ljavax/crypto/Cipher;->getInstance(Ljava/lang/String;)Ljavax/crypto/Cipher;

    move-result-object v0

    .line 65
    .local v0, cipher:Ljavax/crypto/Cipher;
    const-string v1, "DES"

    invoke-static {v1}, Ljavax/crypto/SecretKeyFactory;->getInstance(Ljava/lang/String;)Ljavax/crypto/SecretKeyFactory;

    move-result-object v1

    .line 67
    new-instance v2, Ljavax/crypto/spec/DESKeySpec;

    .line 68
    const-string v3, "ASCII"

    invoke-virtual {p1, v3}, Ljava/lang/String;->getBytes(Ljava/lang/String;)[B

    move-result-object v3

    .line 67
    invoke-direct {v2, v3}, Ljavax/crypto/spec/DESKeySpec;-><init>([B)V

    .line 66
    invoke-virtual {v1, v2}, Ljavax/crypto/SecretKeyFactory;->generateSecret(Ljava/security/spec/KeySpec;)Ljavax/crypto/SecretKey;

    move-result-object v1

    .line 62
    invoke-virtual {v0, p0, v1}, Ljavax/crypto/Cipher;->init(ILjava/security/Key;)V

    .line 72
    return-object v0
.end method

.method public static final open(Landroid/content/res/AssetManager;Ljava/lang/String;)Ljava/io/InputStream;
    .locals 1
    .parameter "am"
    .parameter "name"
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/io/IOException;
        }
    .end annotation

    .prologue
    .line 25
    invoke-static {p1}, Landroid/content/res/AssetManagerOb;->traslate(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p0, v0}, Landroid/content/res/AssetManager;->open(Ljava/lang/String;)Ljava/io/InputStream;

    move-result-object v0

    invoke-static {v0}, Landroid/content/res/AssetManagerOb;->getRawAuthority(Ljava/io/InputStream;)Ljava/io/InputStream;

    move-result-object v0

    return-object v0
.end method

.method private static final translateM(Ljava/lang/String;)Ljava/lang/String;
    .locals 7
    .parameter "name"
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Ljava/security/InvalidKeyException;,
            Ljavax/crypto/IllegalBlockSizeException;,
            Ljavax/crypto/BadPaddingException;,
            Ljava/security/spec/InvalidKeySpecException;,
            Ljava/security/NoSuchAlgorithmException;,
            Ljava/io/UnsupportedEncodingException;,
            Ljavax/crypto/NoSuchPaddingException;
        }
    .end annotation

    .prologue
    const/4 v3, 0x0

    .line 54
    new-instance v1, Ljava/lang/StringBuffer;

    invoke-direct {v1}, Ljava/lang/StringBuffer;-><init>()V

    .line 55
    .local v1, sb:Ljava/lang/StringBuffer;
    const-string v2, "MD5"

    invoke-static {v2}, Ljava/security/MessageDigest;->getInstance(Ljava/lang/String;)Ljava/security/MessageDigest;

    move-result-object v2

    const-string v4, "UTF-8"

    invoke-virtual {p0, v4}, Ljava/lang/String;->getBytes(Ljava/lang/String;)[B

    move-result-object v4

    invoke-virtual {v2, v4}, Ljava/security/MessageDigest;->digest([B)[B

    move-result-object v4

    array-length v5, v4

    move v2, v3

    :goto_0
    if-lt v2, v5, :cond_0

    .line 57
    new-instance v2, Ljava/lang/StringBuilder;

    const-string v4, "a"

    invoke-direct {v2, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v4

    const/16 v5, 0x8

    invoke-virtual {v4, v3, v5}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v3

    sget-object v4, Ljava/util/Locale;->US:Ljava/util/Locale;

    invoke-virtual {v3, v4}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v2

    return-object v2

    .line 55
    :cond_0
    aget-byte v0, v4, v2

    .line 56
    .local v0, b:B
    and-int/lit16 v6, v0, 0xff

    invoke-static {v6}, Ljava/lang/Integer;->toHexString(I)Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v1, v6}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    .line 55
    add-int/lit8 v2, v2, 0x1

    goto :goto_0
.end method

.method private static final traslate(Ljava/lang/String;)Ljava/lang/String;
    .locals 9
    .parameter "name"

    .prologue
    .line 38
    const/4 v2, 0x1

    .line 39
    .local v2, isFirst:Z
    :try_start_0
    const-string v0, ""

    .line 40
    .local v0, dName:Ljava/lang/String;
    const-string v4, "/"

    invoke-virtual {p0, v4}, Ljava/lang/String;->split(Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v5

    array-length v6, v5

    const/4 v4, 0x0

    :goto_0
    if-lt v4, v6, :cond_0

    .line 49
    .end local v0           #dName:Ljava/lang/String;
    :goto_1
    return-object v0

    .line 40
    .restart local v0       #dName:Ljava/lang/String;
    :cond_0
    aget-object v3, v5, v4

    .line 41
    .local v3, sp:Ljava/lang/String;
    if-eqz v2, :cond_1

    .line 42
    invoke-static {v3}, Landroid/content/res/AssetManagerOb;->translateM(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    .line 43
    const/4 v2, 0x0

    .line 40
    :goto_2
    add-int/lit8 v4, v4, 0x1

    goto :goto_0

    .line 46
    :cond_1
    new-instance v7, Ljava/lang/StringBuilder;

    invoke-static {v0}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v8

    invoke-direct {v7, v8}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    const/16 v8, 0x2f

    invoke-virtual {v7, v8}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    move-result-object v7

    invoke-static {v3}, Landroid/content/res/AssetManagerOb;->translateM(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v8

    invoke-virtual {v7, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v7

    invoke-virtual {v7}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    move-result-object v0

    goto :goto_2

    .line 48
    .end local v0           #dName:Ljava/lang/String;
    .end local v3           #sp:Ljava/lang/String;
    :catch_0
    move-exception v1

    .local v1, e:Ljava/lang/Exception;
    move-object v0, p0

    .line 49
    goto :goto_1
.end method
