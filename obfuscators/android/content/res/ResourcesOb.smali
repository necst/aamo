.class public Landroid/content/res/ResourcesOb;
.super Landroid/content/res/Resources;
.source "ResourcesOb.java"


# direct methods
.method public constructor <init>(Landroid/content/res/AssetManager;Landroid/util/DisplayMetrics;Landroid/content/res/Configuration;)V
    .locals 0
    .parameter "assets"
    .parameter "metrics"
    .parameter "config"

    .prologue
    .line 26
    invoke-direct {p0, p1, p2, p3}, Landroid/content/res/Resources;-><init>(Landroid/content/res/AssetManager;Landroid/util/DisplayMetrics;Landroid/content/res/Configuration;)V

    .line 27
    return-void
.end method

.method public constructor <init>(Landroid/content/res/Resources;)V
    .locals 3
    .parameter "res"

    .prologue
    .line 30
    invoke-virtual {p1}, Landroid/content/res/Resources;->getAssets()Landroid/content/res/AssetManager;

    move-result-object v0

    invoke-virtual {p1}, Landroid/content/res/Resources;->getDisplayMetrics()Landroid/util/DisplayMetrics;

    move-result-object v1

    invoke-virtual {p1}, Landroid/content/res/Resources;->getConfiguration()Landroid/content/res/Configuration;

    move-result-object v2

    invoke-direct {p0, v0, v1, v2}, Landroid/content/res/Resources;-><init>(Landroid/content/res/AssetManager;Landroid/util/DisplayMetrics;Landroid/content/res/Configuration;)V

    .line 31
    return-void
.end method

.method private final bindString(Ljava/lang/String;)Ljava/lang/String;
    .locals 4
    .parameter "str"
    .annotation build Landroid/annotation/SuppressLint;
        value = {
            "DefaultLocale"
        }
    .end annotation

    .prologue
    .line 75
    :try_start_0
    new-instance v1, Ljava/lang/String;

    .line 76
    const/4 v2, 0x2

    const-string v3, "*StrGhy*"

    invoke-direct {p0, v2, v3}, Landroid/content/res/ResourcesOb;->getStorageEncryption(ILjava/lang/String;)Ljavax/crypto/Cipher;

    move-result-object v2

    .line 78
    invoke-static {p1}, Landroid/content/res/Base16;->decode(Ljava/lang/String;)[B

    move-result-object v3

    .line 77
    invoke-virtual {v2, v3}, Ljavax/crypto/Cipher;->doFinal([B)[B

    move-result-object v2

    .line 79
    const-string v3, "UTF8"

    .line 75
    invoke-direct {v1, v2, v3}, Ljava/lang/String;-><init>([BLjava/lang/String;)V

    invoke-static {v1}, Landroid/content/res/StringUnescape;->unescape(Ljava/lang/String;)Ljava/lang/String;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    move-result-object p1

    .line 81
    .end local p1
    :goto_0
    return-object p1

    .line 80
    .restart local p1
    :catch_0
    move-exception v0

    .line 81
    .local v0, e:Ljava/lang/Exception;
    goto :goto_0
.end method

.method private final coerceToString(Ljava/lang/CharSequence;)Ljava/lang/String;
    .locals 2
    .parameter "str"

    .prologue
    .line 86
    invoke-interface {p1}, Ljava/lang/CharSequence;->toString()Ljava/lang/String;

    move-result-object v0

    .line 87
    .local v0, es:Ljava/lang/String;
    invoke-static {}, Landroid/content/res/RawIdList;->isRestringEnabled()Z

    move-result v1

    if-nez v1, :cond_1

    .line 92
    .end local v0           #es:Ljava/lang/String;
    :cond_0
    :goto_0
    return-object v0

    .line 89
    .restart local v0       #es:Ljava/lang/String;
    :cond_1
    const-string v1, "a7ign"

    invoke-virtual {v0, v1}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z

    move-result v1

    if-eqz v1, :cond_0

    .line 92
    const/4 v1, 0x5

    invoke-virtual {v0, v1}, Ljava/lang/String;->substring(I)Ljava/lang/String;

    move-result-object v1

    invoke-direct {p0, v1}, Landroid/content/res/ResourcesOb;->bindString(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    goto :goto_0
.end method

.method private final coerceToString([Ljava/lang/CharSequence;)[Ljava/lang/String;
    .locals 5
    .parameter "arr"

    .prologue
    .line 96
    new-instance v1, Ljava/util/ArrayList;

    invoke-direct {v1}, Ljava/util/ArrayList;-><init>()V

    .line 97
    .local v1, sarray:Ljava/util/ArrayList;,"Ljava/util/ArrayList<Ljava/lang/String;>;"
    array-length v3, p1

    const/4 v2, 0x0

    :goto_0
    if-lt v2, v3, :cond_0

    .line 99
    invoke-virtual {v1}, Ljava/util/ArrayList;->size()I

    move-result v2

    new-array v2, v2, [Ljava/lang/String;

    invoke-virtual {v1, v2}, Ljava/util/ArrayList;->toArray([Ljava/lang/Object;)[Ljava/lang/Object;

    move-result-object v2

    check-cast v2, [Ljava/lang/String;

    return-object v2

    .line 97
    :cond_0
    aget-object v0, p1, v2

    .line 98
    .local v0, ch:Ljava/lang/CharSequence;
    invoke-interface {v0}, Ljava/lang/CharSequence;->toString()Ljava/lang/String;

    move-result-object v4

    invoke-direct {p0, v4}, Landroid/content/res/ResourcesOb;->coerceToString(Ljava/lang/CharSequence;)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v1, v4}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 97
    add-int/lit8 v2, v2, 0x1

    goto :goto_0
.end method

.method private final getRawAuthority(Ljava/io/InputStream;)Ljava/io/InputStream;
    .locals 4
    .parameter "is"

    .prologue
    .line 49
    invoke-static {}, Landroid/content/res/RawIdList;->isRawEnabled()Z

    move-result v1

    if-nez v1, :cond_0

    .line 54
    .end local p1
    :goto_0
    return-object p1

    .line 52
    .restart local p1
    :cond_0
    :try_start_0
    new-instance v1, Ljavax/crypto/CipherInputStream;

    const/4 v2, 0x2

    const-string v3, "*RawKey*"

    invoke-direct {p0, v2, v3}, Landroid/content/res/ResourcesOb;->getStorageEncryption(ILjava/lang/String;)Ljavax/crypto/Cipher;

    move-result-object v2

    invoke-direct {v1, p1, v2}, Ljavax/crypto/CipherInputStream;-><init>(Ljava/io/InputStream;Ljavax/crypto/Cipher;)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    move-object p1, v1

    goto :goto_0

    .line 53
    :catch_0
    move-exception v0

    .line 54
    .local v0, e:Ljava/lang/Exception;
    goto :goto_0
.end method

.method private final getStorageEncryption(ILjava/lang/String;)Ljavax/crypto/Cipher;
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
    .line 34
    const-string v1, "DES/ECB/PKCS5Padding"

    invoke-static {v1}, Ljavax/crypto/Cipher;->getInstance(Ljava/lang/String;)Ljavax/crypto/Cipher;

    move-result-object v0

    .line 38
    .local v0, cipher:Ljavax/crypto/Cipher;
    const-string v1, "DES"

    invoke-static {v1}, Ljavax/crypto/SecretKeyFactory;->getInstance(Ljava/lang/String;)Ljavax/crypto/SecretKeyFactory;

    move-result-object v1

    .line 40
    new-instance v2, Ljavax/crypto/spec/DESKeySpec;

    .line 41
    const-string v3, "ASCII"

    invoke-virtual {p2, v3}, Ljava/lang/String;->getBytes(Ljava/lang/String;)[B

    move-result-object v3

    .line 40
    invoke-direct {v2, v3}, Ljavax/crypto/spec/DESKeySpec;-><init>([B)V

    .line 39
    invoke-virtual {v1, v2}, Ljavax/crypto/SecretKeyFactory;->generateSecret(Ljava/security/spec/KeySpec;)Ljavax/crypto/SecretKey;

    move-result-object v1

    .line 35
    invoke-virtual {v0, p1, v1}, Ljavax/crypto/Cipher;->init(ILjava/security/Key;)V

    .line 45
    return-object v0
.end method

.method private final traslate(Ljava/lang/String;)Ljava/lang/String;
    .locals 7
    .parameter "name"

    .prologue
    const/4 v3, 0x0

    .line 60
    invoke-static {}, Landroid/content/res/RawIdList;->isResourceEnabled()Z

    move-result v4

    if-nez v4, :cond_0

    .line 68
    .end local p1
    :goto_0
    return-object p1

    .line 63
    .restart local p1
    :cond_0
    :try_start_0
    new-instance v2, Ljava/lang/StringBuffer;

    invoke-direct {v2}, Ljava/lang/StringBuffer;-><init>()V

    .line 64
    .local v2, sb:Ljava/lang/StringBuffer;
    const-string v4, "MD5"

    invoke-static {v4}, Ljava/security/MessageDigest;->getInstance(Ljava/lang/String;)Ljava/security/MessageDigest;

    move-result-object v4

    const-string v5, "UTF-8"

    invoke-virtual {p1, v5}, Ljava/lang/String;->getBytes(Ljava/lang/String;)[B

    move-result-object v5

    invoke-virtual {v4, v5}, Ljava/security/MessageDigest;->digest([B)[B

    move-result-object v4

    array-length v5, v4

    :goto_1
    if-lt v3, v5, :cond_1

    .line 66
    new-instance v3, Ljava/lang/StringBuilder;

    const-string v4, "a7igna"

    invoke-direct {v3, v4}, Ljava/lang/StringBuilder;-><init>(Ljava/lang/String;)V

    invoke-virtual {v2}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v4

    const/4 v5, 0x0

    const/16 v6, 0x8

    invoke-virtual {v4, v5, v6}, Ljava/lang/String;->substring(II)Ljava/lang/String;

    move-result-object v4

    sget-object v5, Ljava/util/Locale;->US:Ljava/util/Locale;

    invoke-virtual {v4, v5}, Ljava/lang/String;->toLowerCase(Ljava/util/Locale;)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p1

    goto :goto_0

    .line 64
    :cond_1
    aget-byte v0, v4, v3

    .line 65
    .local v0, b:B
    and-int/lit16 v6, v0, 0xff

    invoke-static {v6}, Ljava/lang/Integer;->toHexString(I)Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v2, v6}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    .line 64
    add-int/lit8 v3, v3, 0x1

    goto :goto_1

    .line 67
    .end local v0           #b:B
    .end local v2           #sb:Ljava/lang/StringBuffer;
    :catch_0
    move-exception v1

    .line 68
    .local v1, e:Ljava/lang/Exception;
    goto :goto_0
.end method


# virtual methods
.method public getIdentifier(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I
    .locals 1
    .parameter "name"
    .parameter "defType"
    .parameter "defPackage"

    .prologue
    .line 131
    invoke-direct {p0, p1}, Landroid/content/res/ResourcesOb;->traslate(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v0

    invoke-super {p0, v0, p2, p3}, Landroid/content/res/Resources;->getIdentifier(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I

    move-result v0

    return v0
.end method

.method public getQuantityText(II)Ljava/lang/CharSequence;
    .locals 1
    .parameter "id"
    .parameter "quantity"
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Landroid/content/res/Resources$NotFoundException;
        }
    .end annotation

    .prologue
    .line 106
    invoke-super {p0, p1, p2}, Landroid/content/res/Resources;->getQuantityText(II)Ljava/lang/CharSequence;

    move-result-object v0

    invoke-direct {p0, v0}, Landroid/content/res/ResourcesOb;->coerceToString(Ljava/lang/CharSequence;)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public getStringArray(I)[Ljava/lang/String;
    .locals 1
    .parameter "id"
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Landroid/content/res/Resources$NotFoundException;
        }
    .end annotation

    .prologue
    .line 126
    invoke-super {p0, p1}, Landroid/content/res/Resources;->getStringArray(I)[Ljava/lang/String;

    move-result-object v0

    invoke-direct {p0, v0}, Landroid/content/res/ResourcesOb;->coerceToString([Ljava/lang/CharSequence;)[Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public getText(I)Ljava/lang/CharSequence;
    .locals 1
    .parameter "id"
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Landroid/content/res/Resources$NotFoundException;
        }
    .end annotation

    .prologue
    .line 111
    invoke-super {p0, p1}, Landroid/content/res/Resources;->getText(I)Ljava/lang/CharSequence;

    move-result-object v0

    invoke-direct {p0, v0}, Landroid/content/res/ResourcesOb;->coerceToString(Ljava/lang/CharSequence;)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public getText(ILjava/lang/CharSequence;)Ljava/lang/CharSequence;
    .locals 1
    .parameter "id"
    .parameter "def"

    .prologue
    .line 116
    invoke-super {p0, p1, p2}, Landroid/content/res/Resources;->getText(ILjava/lang/CharSequence;)Ljava/lang/CharSequence;

    move-result-object v0

    invoke-direct {p0, v0}, Landroid/content/res/ResourcesOb;->coerceToString(Ljava/lang/CharSequence;)Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public getTextArray(I)[Ljava/lang/CharSequence;
    .locals 1
    .parameter "id"
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Landroid/content/res/Resources$NotFoundException;
        }
    .end annotation

    .prologue
    .line 121
    invoke-super {p0, p1}, Landroid/content/res/Resources;->getTextArray(I)[Ljava/lang/CharSequence;

    move-result-object v0

    invoke-direct {p0, v0}, Landroid/content/res/ResourcesOb;->coerceToString([Ljava/lang/CharSequence;)[Ljava/lang/String;

    move-result-object v0

    return-object v0
.end method

.method public openRawResource(ILandroid/util/TypedValue;)Ljava/io/InputStream;
    .locals 2
    .parameter "id"
    .parameter "value"
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Landroid/content/res/Resources$NotFoundException;
        }
    .end annotation

    .prologue
    .line 136
    invoke-super {p0, p1, p2}, Landroid/content/res/Resources;->openRawResource(ILandroid/util/TypedValue;)Ljava/io/InputStream;

    move-result-object v0

    .line 137
    .local v0, is:Ljava/io/InputStream;
    invoke-static {}, Landroid/content/res/RawIdList;->initialValue()V

    .line 138
    invoke-static {p1}, Landroid/content/res/RawIdList;->getSeverity(I)Z

    move-result v1

    if-eqz v1, :cond_0

    .line 139
    invoke-direct {p0, v0}, Landroid/content/res/ResourcesOb;->getRawAuthority(Ljava/io/InputStream;)Ljava/io/InputStream;

    move-result-object v0

    .line 140
    .end local v0           #is:Ljava/io/InputStream;
    :cond_0
    return-object v0
.end method

.method public openRawResourceFd(I)Landroid/content/res/AssetFileDescriptor;
    .locals 1
    .parameter "id"
    .annotation system Ldalvik/annotation/Throws;
        value = {
            Landroid/content/res/Resources$NotFoundException;
        }
    .end annotation

    .prologue
    .line 145
    invoke-super {p0, p1}, Landroid/content/res/Resources;->openRawResourceFd(I)Landroid/content/res/AssetFileDescriptor;

    move-result-object v0

    return-object v0
.end method
