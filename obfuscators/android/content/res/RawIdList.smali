.class public final Landroid/content/res/RawIdList;
.super Ljava/lang/Object;
.source "RawIdList.java"


# static fields
.field private static final listIterator:Ljava/util/ArrayList;
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "Ljava/util/ArrayList",
            "<",
            "Ljava/lang/Integer;",
            ">;"
        }
    .end annotation
.end field


# direct methods
.method static constructor <clinit>()V
    .locals 1

    .prologue
    .line 7
    new-instance v0, Ljava/util/ArrayList;

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    sput-object v0, Landroid/content/res/RawIdList;->listIterator:Ljava/util/ArrayList;

    .line 5
    return-void
.end method

.method public constructor <init>()V
    .locals 0

    .prologue
    .line 5
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method private static final add(I)V
    .locals 2
    .parameter "id"

    .prologue
    .line 28
    sget-object v0, Landroid/content/res/RawIdList;->listIterator:Ljava/util/ArrayList;

    invoke-static {p0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    .line 29
    return-void
.end method

.method public static final getSeverity(I)Z
    .locals 2
    .parameter "id"

    .prologue
    .line 32
    sget-object v0, Landroid/content/res/RawIdList;->listIterator:Ljava/util/ArrayList;

    invoke-static {p0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/util/ArrayList;->contains(Ljava/lang/Object;)Z

    move-result v0

    return v0
.end method

.method public static final initialValue()V
    .locals 1

    .prologue
    .line 10
    sget-object v0, Landroid/content/res/RawIdList;->listIterator:Ljava/util/ArrayList;

    invoke-virtual {v0}, Ljava/util/ArrayList;->clear()V

    #RawList

    .line 13
    return-void
.end method

.method public static final isRawEnabled()Z
    .locals 1

    .prologue
    .line 16
    const/4 v0, 0x0 #Raw

    return v0
.end method

.method public static final isResourceEnabled()Z
    .locals 1

    .prologue
    .line 24
    const/4 v0, 0x0 #Res

    return v0
.end method

.method public static final isRestringEnabled()Z
    .locals 1

    .prologue
    .line 20
    const/4 v0, 0x0 #Str

    return v0
.end method
