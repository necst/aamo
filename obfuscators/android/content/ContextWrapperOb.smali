.class public Landroid/content/ContextWrapperOb;
.super Landroid/content/ContextWrapper;
.source "ContextWrapperOb.java"


# direct methods
.method public constructor <init>(Landroid/content/Context;)V
    .locals 0
    .parameter "base"

    .prologue
    .line 9
    invoke-direct {p0, p1}, Landroid/content/ContextWrapper;-><init>(Landroid/content/Context;)V

    .line 10
    return-void
.end method


# virtual methods
.method public getResources()Landroid/content/res/Resources;
    .locals 2

    .prologue
    .line 15
    new-instance v0, Landroid/content/res/ResourcesOb;

    invoke-super {p0}, Landroid/content/ContextWrapper;->getResources()Landroid/content/res/Resources;

    move-result-object v1

    invoke-direct {v0, v1}, Landroid/content/res/ResourcesOb;-><init>(Landroid/content/res/Resources;)V

    return-object v0
.end method
