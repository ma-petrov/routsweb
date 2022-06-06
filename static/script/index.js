const collectionCards = document.getElementsByClassName("collection-card-background");

if (collectionCards.length > 0) {
    function applyResizing(collectionCards, parentWidth, n) {
        let width = "180px";
        if (n != 4) {
            width = ((parentWidth - 20 * n) / n).toString() + "px";
        }
        [...collectionCards].forEach(card => {card.style.width = width;});
    }

    function resizeCollectionCards() {
        const parentWidth = collectionCards[0].parentElement.offsetWidth;
        let n = 4;
        if (parentWidth < 800) {
            n = 1;
            if (parentWidth > 600) {
                n = 3;
            }
            else if (parentWidth > 400) {
                n = 2;
            }
        }
        applyResizing(collectionCards, parentWidth, n);
    }

    window.onresize = resizeCollectionCards;
}

window.onload = () => {
    if (collectionCards.length > 0) {
        [...collectionCards].forEach(item => {
            item.style.backgroundImage = item.id;
        });
        resizeCollectionCards();
    }

    document.getElementById("home-button").style.display = "none";
    document.getElementById("back-button").style.display = "none";
}