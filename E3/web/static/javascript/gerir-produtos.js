const addBtn = document.getElementById("add");
const delBtn = document.getElementById("delete");
const form = document.querySelector("form");

const onChangeDel = (e) => {
  if (delBtn.checked) {
    const prevFieldset = document.querySelector("fieldset");
    if (prevFieldset) prevFieldset.remove();

    const fieldset = document.createElement("fieldset");
    const label = document.createElement("label");
    const input = document.createElement("input");
    const submit = document.createElement("input");
    const br = Array.apply(0, Array(2)).map(() => document.createElement("br"));

    submit.type = "submit";
    submit.value = "Submit";

    label.for = "id";
    label.id = "id-label";
    label.innerHTML = "SKU";
    input.type = "text";
    input.id = "id";
    input.setAttribute("required", "");

    fieldset.appendChild(label);
    fieldset.appendChild(br[0]);
    fieldset.appendChild(input);
    fieldset.appendChild(br[1]);

    fieldset.appendChild(submit);

    form.appendChild(fieldset);
  }
};

const onChangeAdd = (e) => {
  if (addBtn.checked) {
    const prevFieldset = document.querySelector("fieldset");
    if (prevFieldset) prevFieldset.remove();

    const fieldset = document.createElement("fieldset");
    const skuLabel = document.createElement("label");
    const skuInput = document.createElement("input");
    const nameLabel = document.createElement("label");
    const nameInput = document.createElement("input");
    const descriptionLabel = document.createElement("label");
    const descriptionInput = document.createElement("input");
    const priceLabel = document.createElement("label");
    const priceInput = document.createElement("input");
    const submit = document.createElement("input");
    const br = Array.apply(0, Array(8)).map(() => document.createElement("br"));

    submit.type = "submit";
    submit.value = "Submit";

    skuLabel.for = "sku";
    skuLabel.id = "sku-label";
    skuLabel.innerHTML = "SKU";
    skuInput.type = "text";
    skuInput.id = "sku";
    skuInput.setAttribute("required", "");

    nameLabel.for = "name";
    nameLabel.id = "name-label";
    nameLabel.innerHTML = "Name";
    nameInput.type = "text";
    nameInput.id = "name";
    nameInput.setAttribute("required", "");

    descriptionLabel.for = "description";
    descriptionLabel.id = "description-label";
    descriptionLabel.innerHTML = "Description";
    descriptionInput.type = "text";
    descriptionInput.id = "description";
    descriptionInput.setAttribute("required", "");

    priceLabel.for = "price";
    priceLabel.id = "price-label";
    priceLabel.innerHTML = "Price";
    priceInput.type = "number";
    priceInput.id = "price";
    priceInput.setAttribute("required", "");

    fieldset.appendChild(skuLabel);
    fieldset.appendChild(br[0]);
    fieldset.appendChild(skuInput);
    fieldset.appendChild(br[1]);

    fieldset.appendChild(nameLabel);
    fieldset.appendChild(br[2]);
    fieldset.appendChild(nameInput);
    fieldset.appendChild(br[3]);

    fieldset.appendChild(descriptionLabel);
    fieldset.appendChild(br[4]);
    fieldset.appendChild(descriptionInput);
    fieldset.appendChild(br[5]);

    fieldset.appendChild(priceLabel);
    fieldset.appendChild(br[6]);
    fieldset.appendChild(priceInput);
    fieldset.appendChild(br[7]);

    fieldset.appendChild(submit);

    form.appendChild(fieldset);
  }
};

delBtn.addEventListener("change", onChangeDel);
addBtn.addEventListener("change", onChangeAdd);
