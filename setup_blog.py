import os, zipfile, requests

print("🔧 ERLPBLOG kuruluyor...")

# --- DEMO GÖRSEL İNDİRME ---
os.makedirs("assets/uploads", exist_ok=True)
img_url = "https://picsum.photos/800/500"
img_path = "assets/uploads/sample.jpg"
with open(img_path, "wb") as f:
    f.write(requests.get(img_url).content)

# --- DOSYALAR ---
files = {
"index.html": """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>Blog</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>

<header>
<h1>ERLP Blog</h1>
</header>

<main id="posts"></main>

<script src="https://cdn.jsdelivr.net/npm/showdown/dist/showdown.min.js"></script>
<script src="assets/script.js"></script>

</body>
</html>
""",

"post.html": """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>Blog Yazısı</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>

<a href="index.html" class="back">← Anasayfa</a>
<main id="content">Yükleniyor...</main>

<div id="disqus_thread"></div>
<script>
var disqus_config = function () {};
(function() {
var d = document, s = d.createElement('script');
s.src = 'https://erlpblog.disqus.com/embed.js';
s.setAttribute('data-timestamp', +new Date());
(d.head || d.body).appendChild(s);
})();
</script>

<script src="https://cdn.jsdelivr.net/npm/showdown/dist/showdown.min.js"></script>
<script>
async function loadPost(){
const p=new URLSearchParams(location.search);
const f=p.get("post");
const r=await fetch("posts/"+f);
const t=await r.text();
const c=new showdown.Converter();
document.getElementById("content").innerHTML=c.makeHtml(t);
}
loadPost();
</script>

</body>
</html>
""",

"assets/style.css": """body{margin:0;font-family:Arial;background:#111;color:#eee;}
header{background:#222;padding:20px;text-align:center;}
h1{margin:0;color:#49b6ff;}
#posts{padding:20px;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:20px;}
.card{background:#1a1a1a;padding:15px;border-radius:10px;transition:.2s;}
.card:hover{transform:scale(1.04);}
.thumb{width:100%;border-radius:10px;}
.card h2{color:#4fc2ff;}
.back{display:inline-block;margin:20px;color:#4fc2ff;text-decoration:none;}
#content img{max-width:100%;border-radius:10px;}
""",

"assets/script.js": """async function loadPosts(){
const posts=document.getElementById("posts");
const html=await (await fetch("posts/")).text();
const files=[...html.matchAll(/href=\\"(.*?\\.md)\\"/g)].map(m=>m[1]);
let out="";
for(const f of files){
const t=await (await fetch("posts/"+f)).text();
const title=t.match(/title:\\s*(.*)/)?.[1]||f;
const img=t.match(/image:\\s*(.*)/)?.[1];
const cat=t.match(/category:\\s*(.*)/)?.[1];
out+=`<div class="card">
${img?`<img src="${img}" class="thumb">`:""}
<h2><a href="post.html?post=${f}">${title}</a></h2>
<p>Kategori: ${cat||"Genel"}</p>
</div>`;}
posts.innerHTML=out;}
loadPosts();
""",

"posts/ilk-yazi.md": """---
title: İlk Blog Yazım
date: 2025-01-01
image: /assets/uploads/sample.jpg
category: Genel
---

# Merhaba!

Bu blog artık:

✔ Modern tema  
✔ Kategoriler  
✔ Görsel desteği  
✔ Yorum sistemi  

hepsiyle birlikte çalışıyor!
""",

"admin/index.html": """<!DOCTYPE html>
<html><head><meta charset="utf-8"/>
<title>Admin</title>
<script src="https://unpkg.com/@staticcms/core/dist/static-cms-app.js"></script>
</head>
<body><script>CMS.init();</script></body>
</html>
""",

"admin/config.yml": """backend:
  name: github
  repo: daemon149/erlpblog
  branch: main

media_folder: "assets/uploads"
public_folder: "/assets/uploads"

collections:
  - name: "posts"
    label: "Yazılar"
    folder: "posts"
    create: true
    slug: "{{slug}}"
    format: "frontmatter"
    fields:
      - { label: "Başlık", name: "title", widget: "string" }
      - { label: "Kapak Görseli", name: "image", widget: "image", required: false }
      - { label: "Kategori", name: "category", widget: "select", options: ["Genel","Oyun","Günlük","Kodlama"] }
      - { label: "Tarih", name: "date", widget: "datetime" }
      - { label: "İçerik", name: "body", widget: "markdown" }
"""
}

# --- KLASÖR VE DOSYA YAZMA ---
for path, content in files.items():
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# --- ZIP OLUŞTUR ---
zip_name = "erlpblog.zip"
with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, fs in os.walk("."):
        for file in fs:
            if file != zip_name:
                z.write(os.path.join(root, file))

print("🎉 erlpblog.zip başarıyla oluşturuldu!")
