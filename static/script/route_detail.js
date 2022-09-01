[...document.getElementsByClassName("gallery-image")].forEach(e => {
    console.log(`photo ${e.src}`);
    e.addEventListener("click", target => {
        console.log(target.style.src);
    });
});

console.log("hui");

document.onload = () => {console.log("hui");}