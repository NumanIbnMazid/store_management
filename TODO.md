
# Project Estimated Duration: 13-09-2021 to 20-10-2021

# 1st step questionnaire's answers arrived at 21-09-2021

# TODO: API: Plan Create => Option (Multi select Field), Fix Relation Type

# TODO: API: Fix All Image Fields and convert to base64

# TODO: API: Create, Update Studio Calendar Custom Holidays

# TODO: API: Manage Studio Business Hour, Regular Holiday Registration Edit by Day of Week

# TODO: API: Manage Notification

# TODO: API: Tax Management

# TODO: API: Collective Deal Management

# TODO: BUG: Same Plan can be on multiple space (Fixed)

# TODO: Slug is blank while studio name is japanese

# TODO: Staff permission check if in accessing studio

# TODO: BUG: Same Plan can be on multiple space

# Notifications fields id, title, slug, display_date, display_time(null_able), message, link_url, pdf_link, file(base64), is_published(default=False), studio, created_at, update_at

# Get active notifications list only petch is_published

# Crud manage celery or cron jobs for every crud

# Currency Model, Inherit everywhere where amount or cost is used

# TODO: validate default_closing_days in store create from serializer (Done)

# TODO: terminate loop imidiately if found an element in business day checker within check business day exists for year

# TODO: BUG: django.db.utils.DataError: value too long for type character varying(27) : check business day API

# studio:{
    "store":["studio all store"
    ],
}

# Get all studio list 

# TODO: name valdiation with case(Upper, lower), SLug with UUID, studio-> User {} : validation, This field is required -> field name is required, User validatoin and studio validation raise together.

# Numan bhai can you check the Plan models I'm not able to create a object -- slug uid 
# Staff Module-- Numan bhai how can I get studio staff I see here no relation with staff and studio

# Space many TO Many Save BUG

# Studio Create with User password too short Error response Fix

# IsStoreStaff Permission Fix (Used on VatTax Dynamic List)

# Fix is_studio_admin on Factory Boy Commands

# Studio Modarator qs = Studio.objects.filter(Q(user__slug=request.user.slug) | Q(store_moderators__user__slug=request.user.slug) Permission PY

# BUG: Store Moderator Create with store id [0]

# Bug: Store MOderator Create with different Studio's Store

# Bug Store Moderator Create with empty store

# TODO: Store Moderator Create for System Super Admin => Options: User, Studio, Store (Studio Select API, Stores for Studio (Slug))

# TODO: Permission for System Super Admin (EX: Store Access Permission -> If store selected in other studio's)

# TODO: Image Upload validation with Size, Type

# TODO: Business Hour

# Store Update Validation with Image URL

# This field is required -> Name field is required!

# Currency Foreign Key Where Used In this project

# Uncomment: Permission Class: Space, Require LogginMixin