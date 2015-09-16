.class public final Landroid/content/res/Base16;
.super Ljava/lang/Object;
.source "Base16.java"


# static fields
.field private static final HEX:[C


# direct methods
.method static constructor <clinit>()V
    .locals 1

    .prologue
    .line 5
    const/16 v0, 0x10

    new-array v0, v0, [C

    fill-array-data v0, :array_0

    sput-object v0, Landroid/content/res/Base16;->HEX:[C

    .line 3
    return-void

    .line 5
    :array_0
    .array-data 0x2
        0x30t 0x0t
        0x31t 0x0t
        0x32t 0x0t
        0x33t 0x0t
        0x34t 0x0t
        0x35t 0x0t
        0x36t 0x0t
        0x37t 0x0t
        0x38t 0x0t
        0x39t 0x0t
        0x61t 0x0t
        0x62t 0x0t
        0x63t 0x0t
        0x64t 0x0t
        0x65t 0x0t
        0x66t 0x0t
    .end array-data
.end method

.method public constructor <init>()V
    .locals 0

    .prologue
    .line 3
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static final decode(Ljava/lang/String;)[B
    .locals 10
    .parameter "s"

    .prologue
    const/16 v9, 0x66

    const/16 v8, 0x61

    const/16 v7, 0x39

    const/16 v6, 0x30

    .line 18
    invoke-virtual {p0}, Ljava/lang/String;->length()I

    move-result v3

    .line 19
    .local v3, len:I
    div-int/lit8 v5, v3, 0x2

    new-array v4, v5, [B

    .line 20
    .local v4, r:[B
    const/4 v2, 0x0

    .local v2, i:I
    :goto_0
    array-length v5, v4

    if-lt v2, v5, :cond_0

    .line 33
    return-object v4

    .line 21
    :cond_0
    mul-int/lit8 v5, v2, 0x2

    invoke-virtual {p0, v5}, Ljava/lang/String;->charAt(I)C

    move-result v0

    .local v0, digit1:I
    mul-int/lit8 v5, v2, 0x2

    add-int/lit8 v5, v5, 0x1

    invoke-virtual {p0, v5}, Ljava/lang/String;->charAt(I)C

    move-result v1

    .line 22
    .local v1, digit2:I
    if-lt v0, v6, :cond_3

    if-gt v0, v7, :cond_3

    .line 23
    add-int/lit8 v0, v0, -0x30

    .line 26
    :cond_1
    :goto_1
    if-lt v1, v6, :cond_4

    if-gt v1, v7, :cond_4

    .line 27
    add-int/lit8 v1, v1, -0x30

    .line 31
    :cond_2
    :goto_2
    shl-int/lit8 v5, v0, 0x4

    add-int/2addr v5, v1

    int-to-byte v5, v5

    aput-byte v5, v4, v2

    .line 20
    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    .line 24
    :cond_3
    if-lt v0, v8, :cond_1

    if-gt v0, v9, :cond_1

    .line 25
    add-int/lit8 v0, v0, -0x57

    goto :goto_1

    .line 28
    :cond_4
    if-lt v1, v8, :cond_2

    if-gt v1, v9, :cond_2

    .line 29
    add-int/lit8 v1, v1, -0x57

    goto :goto_2
.end method

.method public static final encode([B)Ljava/lang/String;
    .locals 6
    .parameter "byteArray"

    .prologue
    .line 10
    new-instance v0, Ljava/lang/StringBuffer;

    array-length v3, p0

    mul-int/lit8 v3, v3, 0x2

    invoke-direct {v0, v3}, Ljava/lang/StringBuffer;-><init>(I)V

    .line 11
    .local v0, hexBuffer:Ljava/lang/StringBuffer;
    const/4 v1, 0x0

    .local v1, i:I
    :goto_0
    array-length v3, p0

    if-lt v1, v3, :cond_0

    .line 14
    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v3

    return-object v3

    .line 12
    :cond_0
    const/4 v2, 0x1

    .local v2, j:I
    :goto_1
    if-gez v2, :cond_1

    .line 11
    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    .line 13
    :cond_1
    sget-object v3, Landroid/content/res/Base16;->HEX:[C

    aget-byte v4, p0, v1

    mul-int/lit8 v5, v2, 0x4

    shr-int/2addr v4, v5

    and-int/lit8 v4, v4, 0xf

    aget-char v3, v3, v4

    invoke-virtual {v0, v3}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    .line 12
    add-int/lit8 v2, v2, -0x1

    goto :goto_1
.end method
