//show menu bar

let bar = document.querySelector('.bars');
let menu = document.querySelector('.menu');

bar.addEventListener('click', () => {
    menu.classList.toggle('show-menu');
});

// portfolio category btns

const cateButtons = document.querySelectorAll('.portfolio-tab-btns li');

cateButtons.forEach(cateBtn => {
    cateBtn.addEventListener('click', () => {
        cateButtons.forEach(btn => btn.classList.remove('active-btn'));

        cateBtn.classList.add('active-btn');
    });
});


// poertfolio mixitup

var mixer = mixitup('.portfolio');


// faq section 

const faqCols= document.querySelectorAll('.faq-col');

faqCols.forEach(faqCol =>{
    faqCol.addEventListener('click',() =>{

        const openFaq = document.querySelector('.faq-col.show-ans');
        if(openFaq && openFaq !== faqCol){
            openFaq.classList.remove('show-ans');
            openFaq.querySelector('.ans').classList.remove('show-ans-text');
            const openIcon = openFaq.querySelector('.faq-head i');
            openIcon.classList.remove('ri-subtract-fill','active-faq-icon');
            openIcon.classList.add('ri-add-fill');
        }

        const answer = faqCol.querySelector('.ans');
        const icon = faqCol.querySelector('.faq-head i');
        const isOpen = faqCol.classList.toggle('show-ans');
        answer.classList.toggle('show-ans-text', isOpen);

        icon.classList.toggle('ri-add-fill',  !isOpen);
        icon.classList.toggle('ri-subtract-fill',  isOpen);
        icon.classList.toggle('active-faq-icon',  isOpen);
    });
});
