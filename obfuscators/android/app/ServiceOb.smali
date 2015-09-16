.class public abstract Landroid/app/ServiceOb;
.super Landroid/app/Service;
.source "ServiceOb.java"


# static fields
.field private static mContext:Landroid/content/Context;


# direct methods
.method public constructor <init>()V
    .locals 0

    .prologue
    .line 9
    invoke-direct {p0}, Landroid/app/Service;-><init>()V

    .line 10
    return-void
.end method

.method public static getStaticContext()Landroid/content/Context;
    .locals 1

    .prologue
    .line 25
    sget-object v0, Landroid/app/ServiceOb;->mContext:Landroid/content/Context;

    return-object v0
.end method

.method private static setStaticContext(Landroid/content/Context;)V
    .locals 0
    .parameter "context"

    .prologue
    .line 21
    sput-object p0, Landroid/app/ServiceOb;->mContext:Landroid/content/Context;

    .line 22
    return-void
.end method


# virtual methods
.method protected attachBaseContext(Landroid/content/Context;)V
    .locals 1
    .parameter "base"

    .prologue
    .line 14
    new-instance v0, Landroid/content/ContextWrapperOb;

    invoke-direct {v0, p1}, Landroid/content/ContextWrapperOb;-><init>(Landroid/content/Context;)V

    invoke-super {p0, v0}, Landroid/app/Service;->attachBaseContext(Landroid/content/Context;)V

    .line 15
    invoke-static {p1}, Landroid/app/ServiceOb;->setStaticContext(Landroid/content/Context;)V

    .line 16
    return-void
.end method
