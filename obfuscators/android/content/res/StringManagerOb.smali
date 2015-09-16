.class public Landroid/content/res/StringManagerOb;
.super Ljava/lang/Object;
.source "StringManagerOb.java"


# direct methods
.method public constructor <init>()V
    .locals 0

    .prologue
    .line 13
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static final convertToString(Ljava/lang/String;)Ljava/lang/String;
    .locals 4
    .parameter "str"

    .prologue
    .line 17
    :try_start_0
    new-instance v1, Ljava/lang/String;

    .line 18
    const/4 v2, 0x2

    const-string v3, "*StrGhy*"

    invoke-static {v2, v3}, Landroid/content/res/StringManagerOb;->getStorageEncryption(ILjava/lang/String;)Ljavax/crypto/Cipher;

    move-result-object v2

    .line 20
    invoke-static {p0}, Landroid/content/res/StringManagerOb;->decode(Ljava/lang/String;)[B

    move-result-object v3

    .line 19
    invoke-virtual {v2, v3}, Ljavax/crypto/Cipher;->doFinal([B)[B

    move-result-object v2

    .line 21
    const-string v3, "UTF8"

    .line 17
    invoke-direct {v1, v2, v3}, Ljava/lang/String;-><init>([BLjava/lang/String;)V

    invoke-static {v1}, Landroid/content/res/StringManagerOb;->unescapeJavaString(Ljava/lang/String;)Ljava/lang/String;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    move-result-object p0

    .line 23
    .local v0, e:Ljava/lang/Exception;
    :goto_0
    return-object p0

    .line 22
    .end local v0           #e:Ljava/lang/Exception;
    :catch_0
    move-exception v0

    .line 23
    .restart local v0       #e:Ljava/lang/Exception;
    goto :goto_0
.end method

.method private static final decode(Ljava/lang/String;)[B
    .locals 10
    .parameter "s"

    .prologue
    const/16 v9, 0x66

    const/16 v8, 0x61

    const/16 v7, 0x39

    const/16 v6, 0x30

    .line 28
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v3

    .line 29
    .local v3, len:I
    div-int/lit8 v5, v3, 0x2

    new-array v4, v5, [B

    .line 30
    .local v4, r:[B
    const/4 v2, 0x0

    .local v2, i:I
    :goto_0
    array-length v5, v4

    if-lt v2, v5, :cond_0

    .line 43
    return-object v4

    .line 31
    :cond_0
    mul-int/lit8 v5, v2, 0x2

    invoke-virtual {p0, v5}, Ljava/lang/String;->charAt(I)C

    move-result v0

    .local v0, digit1:I
    mul-int/lit8 v5, v2, 0x2

    add-int/lit8 v5, v5, 0x1

    invoke-virtual {p0, v5}, Ljava/lang/String;->charAt(I)C

    move-result v1

    .line 32
    .local v1, digit2:I
    if-lt v0, v6, :cond_3

    if-gt v0, v7, :cond_3

    .line 33
    add-int/lit8 v0, v0, -0x30

    .line 36
    :cond_1
    :goto_1
    if-lt v1, v6, :cond_4

    if-gt v1, v7, :cond_4

    .line 37
    add-int/lit8 v1, v1, -0x30

    .line 41
    :cond_2
    :goto_2
    shl-int/lit8 v5, v0, 0x4

    add-int/2addr v5, v1

    int-to-byte v5, v5

    aput-byte v5, v4, v2

    .line 30
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    .line 34
    :cond_3
    if-lt v0, v8, :cond_1

    if-gt v0, v9, :cond_1

    .line 35
    add-int/lit8 v0, v0, -0x57

    goto :goto_1

    .line 38
    :cond_4
    if-lt v1, v8, :cond_2

    if-gt v1, v9, :cond_2

    .line 39
    add-int/lit8 v1, v1, -0x57

    goto :goto_2
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
    .line 47
    const-string v1, "DES/ECB/PKCS5Padding"

    invoke-static {v1}, Ljavax/crypto/Cipher;->getInstance(Ljava/lang/String;)Ljavax/crypto/Cipher;

    move-result-object v0

    .line 51
    .local v0, cipher:Ljavax/crypto/Cipher;
    const-string v1, "DES"

    invoke-static {v1}, Ljavax/crypto/SecretKeyFactory;->getInstance(Ljava/lang/String;)Ljavax/crypto/SecretKeyFactory;

    move-result-object v1

    .line 53
    new-instance v2, Ljavax/crypto/spec/DESKeySpec;

    .line 54
    const-string v3, "ASCII"

    invoke-virtual {p1, v3}, Ljava/lang/String;->getBytes(Ljava/lang/String;)[B

    move-result-object v3

    .line 53
    invoke-direct {v2, v3}, Ljavax/crypto/spec/DESKeySpec;-><init>([B)V

    .line 52
    invoke-virtual {v1, v2}, Ljavax/crypto/SecretKeyFactory;->generateSecret(Ljava/security/spec/KeySpec;)Ljavax/crypto/SecretKey;

    move-result-object v1

    .line 48
    invoke-virtual {v0, p0, v1}, Ljavax/crypto/Cipher;->init(ILjava/security/Key;)V

    .line 58
    return-object v0
.end method

.method private static final unescapeJavaString(Ljava/lang/String;)Ljava/lang/String;
    .locals 10
    .parameter "st"

    .prologue
    const/16 v5, 0x5c

    const/16 v9, 0x37

    const/16 v8, 0x30

    .line 63
    new-instance v4, Ljava/lang/StringBuilder;

    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v6

    invoke-direct {v4, v6}, Ljava/lang/StringBuilder;-><init>(I)V

    .line 65
    .local v4, sb:Ljava/lang/StringBuilder;
    const/4 v2, 0x0

    .local v2, i:I
    :goto_0
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v6

    if-lt v2, v6, :cond_0

    .line 127
    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    return-object v5

    .line 66
    :cond_0
    invoke-virtual {p0, v2}, Ljava/lang/String;->charAt(I)C

    move-result v0

    .line 67
    .local v0, ch:C
    if-ne v0, v5, :cond_4

    .line 68
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v6

    add-int/lit8 v6, v6, -0x1

    if-ne v2, v6, :cond_2

    move v3, v5

    .line 70
    .local v3, nextChar:C
    :goto_1
    if-lt v3, v8, :cond_3

    if-gt v3, v9, :cond_3

    .line 71
    new-instance v6, Ljava/lang/StringBuilder;

    invoke-direct {v6}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v6, v3}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    move-result-object v6

    invoke-virtual {v6}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    .line 72
    .local v1, code:Ljava/lang/String;
    add-int/lit8 v2, v2, 0x1

    .line 73
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v6

    add-int/lit8 v6, v6, -0x1

    if-ge v2, v6, :cond_1

    add-int/lit8 v6, v2, 0x1

    invoke-virtual {p0, v6}, Ljava/lang/String;->charAt(I)C

    move-result v6

    if-lt v6, v8, :cond_1

    .line 74
    add-int/lit8 v6, v2, 0x1

    invoke-virtual {p0, v6}, Ljava/lang/String;->charAt(I)C

    move-result v6

    if-gt v6, v9, :cond_1

    .line 75
    new-instance v6, Ljava/lang/StringBuilder;

    invoke-static {v1}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v7

    invoke-direct {v6, v7}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    add-int/lit8 v7, v2, 0x1

    invoke-virtual {p0, v7}, Ljava/lang/String;->charAt(I)C

    move-result v7

    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    move-result-object v6

    invoke-virtual {v6}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    .line 76
    add-int/lit8 v2, v2, 0x1

    .line 77
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v6

    add-int/lit8 v6, v6, -0x1

    if-ge v2, v6, :cond_1

    add-int/lit8 v6, v2, 0x1

    invoke-virtual {p0, v6}, Ljava/lang/String;->charAt(I)C

    move-result v6

    if-lt v6, v8, :cond_1

    .line 78
    add-int/lit8 v6, v2, 0x1

    invoke-virtual {p0, v6}, Ljava/lang/String;->charAt(I)C

    move-result v6

    if-gt v6, v9, :cond_1

    .line 79
    new-instance v6, Ljava/lang/StringBuilder;

    invoke-static {v1}, Ljava/lang/String;->valueOf(Ljava/lang/Object;)Ljava/lang/String;

    move-result-object v7

    invoke-direct {v6, v7}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    add-int/lit8 v7, v2, 0x1

    invoke-virtual {p0, v7}, Ljava/lang/String;->charAt(I)C

    move-result v7

    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    move-result-object v6

    invoke-virtual {v6}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    .line 80
    add-int/lit8 v2, v2, 0x1

    .line 83
    :cond_1
    const/16 v6, 0x8

    invoke-static {v1, v6}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;I)I

    move-result v6

    int-to-char v6, v6

    invoke-virtual {v4, v6}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    .line 65
    .end local v1           #code:Ljava/lang/String;
    .end local v3           #nextChar:C
    :goto_2
    add-int/lit8 v2, v2, 0x1

    goto/16 :goto_0

    .line 69
    :cond_2
    add-int/lit8 v6, v2, 0x1

    invoke-virtual {p0, v6}, Ljava/lang/String;->charAt(I)C

    move-result v3

    goto/16 :goto_1

    .line 86
    .restart local v3       #nextChar:C
    :cond_3
    sparse-switch v3, :sswitch_data_0

    .line 123
    :goto_3
    add-int/lit8 v2, v2, 0x1

    .line 125
    .end local v3           #nextChar:C
    :cond_4
    invoke-virtual {v4, v0}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    goto :goto_2

    .line 88
    .restart local v3       #nextChar:C
    :sswitch_0
    const/16 v0, 0x5c

    .line 89
    goto :goto_3

    .line 91
    :sswitch_1
    const/16 v0, 0x8

    .line 92
    goto :goto_3

    .line 94
    :sswitch_2
    const/16 v0, 0xc

    .line 95
    goto :goto_3

    .line 97
    :sswitch_3
    const/16 v0, 0xa

    .line 98
    goto :goto_3

    .line 100
    :sswitch_4
    const/16 v0, 0xd

    .line 101
    goto :goto_3

    .line 103
    :sswitch_5
    const/16 v0, 0x9

    .line 104
    goto :goto_3

    .line 106
    :sswitch_6
    const/16 v0, 0x22

    .line 107
    goto :goto_3

    .line 109
    :sswitch_7
    const/16 v0, 0x27

    .line 110
    goto :goto_3

    .line 112
    :sswitch_8
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v6

    add-int/lit8 v6, v6, -0x5

    if-lt v2, v6, :cond_5

    .line 113
    const/16 v0, 0x75

    .line 114
    goto :goto_3

    .line 117
    :cond_5
    new-instance v6, Ljava/lang/StringBuilder;

    invoke-direct {v6}, Ljava/lang/StringBuilder;-><init>()V

    add-int/lit8 v7, v2, 0x2

    invoke-virtual {p0, v7}, Ljava/lang/String;->charAt(I)C

    move-result v7

    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    move-result-object v6

    add-int/lit8 v7, v2, 0x3

    invoke-virtual {p0, v7}, Ljava/lang/String;->charAt(I)C

    move-result v7

    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    move-result-object v6

    .line 118
    add-int/lit8 v7, v2, 0x4

    invoke-virtual {p0, v7}, Ljava/lang/String;->charAt(I)C

    move-result v7

    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    move-result-object v6

    add-int/lit8 v7, v2, 0x5

    invoke-virtual {p0, v7}, Ljava/lang/String;->charAt(I)C

    move-result v7

    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    move-result-object v6

    .line 117
    invoke-virtual {v6}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v6

    .line 118
    const/16 v7, 0x10

    .line 116
    invoke-static {v6, v7}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;I)I

    move-result v1

    .line 119
    .local v1, code:I
    invoke-static {v1}, Ljava/lang/Character;->toChars(I)[C

    move-result-object v6

    invoke-virtual {v4, v6}, Ljava/lang/StringBuilder;->append([C)Ljava/lang/StringBuilder;

    .line 120
    add-int/lit8 v2, v2, 0x5

    .line 121
    goto :goto_2

    .line 86
    :sswitch_data_0
    .sparse-switch
        0x22 -> :sswitch_6
        0x27 -> :sswitch_7
        0x5c -> :sswitch_0
        0x62 -> :sswitch_1
        0x66 -> :sswitch_2
        0x6e -> :sswitch_3
        0x72 -> :sswitch_4
        0x74 -> :sswitch_5
        0x75 -> :sswitch_8
    .end sparse-switch
.end method
