async function loadPosts(){
const posts=document.getElementById("posts");
const html=await (await fetch("posts/")).text();
const files=[...html.matchAll(/href=\"(.*?\.md)\"/g)].map(m=>m[1]);
let out="";
for(const f of files){
const t=await (await fetch("posts/"+f)).text();
const title=t.match(/title:\s*(.*)/)?.[1]||f;
const img=t.match(/image:\s*(.*)/)?.[1];
const cat=t.match(/category:\s*(.*)/)?.[1];
out+=`<div class="card">
${img?`<img src="${img}" class="thumb">`:""}
<h2><a href="post.html?post=${f}">${title}</a></h2>
<p>Kategori: ${cat||"Genel"}</p>
</div>`;}
posts.innerHTML=out;}
loadPosts();
