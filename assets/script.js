async function loadProjects() {
  const grid = document.getElementById("project-grid");
  if (!grid) return;

  try {
    const response = await fetch("assets/projects.json");
    const projects = await response.json();

    grid.innerHTML = projects
      .map(
        (project) => `
        <article class="project-card">
          <img src="${project.image}" alt="${project.title} önizleme">
          <p class="project-meta">${project.category}</p>
          <h3>${project.title}</h3>
          <p>${project.description}</p>
          <a class="card-link" href="#contact">Detay iste →</a>
        </article>
      `
      )
      .join("");
  } catch (error) {
    grid.innerHTML = "<p>Projeler yüklenemedi. Lütfen daha sonra tekrar deneyin.</p>";
  }
}

loadProjects();
