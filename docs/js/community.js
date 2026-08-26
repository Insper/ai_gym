(function () {
  "use strict";

  const container = document.getElementById("contributors");
  if (!container) return;

  const contributorPage = "https://github.com/Insper/ai_gym/graphs/contributors";

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
    count.textContent = `${commits} ${commits === 1 ? "contribution" : "contributions"}`;

    details.append(name, count);
    card.append(avatar, details);
    return card;
  }

  fetch("../assets/data/contributors.json")
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
      message.append("Contributor data is temporarily unavailable. ");

      const link = document.createElement("a");
      link.href = contributorPage;
      link.textContent = "View contributors on GitHub.";
      message.append(link);
      container.replaceChildren(message);
    });
})();