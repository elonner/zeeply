const $select = $('select');

const compare = [];
for (opt of $select[0].children) {
    let add = true;
    compare.forEach(val => {
        if (val === opt.value) {
            opt.remove();
            add = false;
        }
    });
    if (add) compare.push(opt.value);
}