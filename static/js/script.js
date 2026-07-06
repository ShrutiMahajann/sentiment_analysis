document.addEventListener("DOMContentLoaded", () => {

    // Animated Counter
    const score = document.getElementById("score");

    if(score){
        const target = parseInt(score.textContent);
        let current = 0;
        const speed = 20;
        const counter = setInterval(() => {
            if(current >= target){
                clearInterval(counter);
            }else{
                current++;
                score.textContent = current + "%";
            }
        },speed);
    }

    // Card Animation
    const cards = document.querySelectorAll(".card,.summary,.box,.sentence-card");
    cards.forEach((card,index)=>{
        card.style.opacity="0";
        card.style.transform="translateY(20px)";
        setTimeout(()=>{
            card.style.transition=".6s ease";
            card.style.opacity="1";
            card.style.transform="translateY(0px)";
        },index*120);

    });

});