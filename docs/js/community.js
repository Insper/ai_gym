(function () {
  "use strict";

  const container = document.getElementById("contributors");
  if (!container) return;

  const contributorPage = "https://github.com/Insper/ai_gym/graphs/contributors";
  const isPortuguese = document.documentElement.lang.startsWith("pt");
  const script = Array.from(document.scripts).find((item) =>
    item.src.endsWith("/js/community.js")
  );
  const contributorData = new URL(
    "../assets/data/contributors.json",
    script ? script.src : document.baseURI,
  );

  function makeCard(contributor) {
    const card = document.createElement("a");
    card.className = "contributor-card";
    card.href = contributor.html_url;
    card.target = "_blank";
    card.rel = "noopener noreferrer";

    const avatar = document.createElement("img");
    avatar.className = "contributor-card__avatar";
    avatar.src = contributor.avatar_url;
    avatar.alt = "";
    avatar.width = 48;
    avatar.height = 48;
    avatar.loading = "lazy";

    const details = document.createElement("span");
    details.className = "contributor-card__details";

    const name = document.createElement("span");
    name.className = "contributor-card__name";
    name.textContent = contributor.login;

    const count = document.createElement("span");
    count.className = "contributor-card__count";
    const commits = contributor.contributions;
    const contributionLabel = isPortuguese
      ? commits === 1
        ? "contribuição"
        : "contribuições"
      : commits === 1
        ? "contribution"
        : "contributions";
    count.textContent = `${commits} ${contributionLabel}`;

    details.append(name, count);
    card.append(avatar, details);
    return card;
  }

  fetch(contributorData)
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then((contributors) => {
      container.replaceChildren(...contributors.map(makeCard));
    })
    .catch(() => {
      const message = document.createElement("p");
      message.className = "contributors__error";
      message.append(
        isPortuguese
          ? "Os dados dos colaboradores estão temporariamente indisponíveis. "
          : "Contributor data is temporarily unavailable. ",
      );

      const link = document.createElement("a");
      link.href = contributorPage;
      link.textContent = isPortuguese
        ? "Ver colaboradores no GitHub."
        : "View contributors on GitHub.";
      message.append(link);
      container.replaceChildren(message);
    });
})();
