var dataurl = "data/movies.json";
var Fields = {
  categ: [
    "MPAA_Rating",
    "Source",
    "Creative_Type",
    "Director",
    "Distributor",
    "Major_Genre",
    "Title",
  ],
  date: ["Release_Date"],
  quant: [
    "IMDB_Rating",
    "IMDB_Votes",
    "Production_Budget",
    "Rotten_Tomatoes_Rating",
    "Running_Time_min",
    "US_DVD_Sales",
    "US_Gross",
    "Worldwide_Gross",
  ],
};

var bookmarkContent = document.querySelector(".bookmark_content");
var fieldLst = document.querySelector(".attr-lst");
var mainImg = document.querySelector(".mainImg");

// names of selected field
var checkedFields = [];
var queryMap = {};
var bookmarked = {};

// document.querySelector("#main_wrapper").style.display = "none";
initial();

function initial() {
  initField(Fields);
}

function addFields(fields) {
  let res = "";
  let enabledstr = "enabled";
  for (e of fields.categ) {
    res += `<li class="categ-attr ${enabledstr}">
                    <div>
                        <i class="fas fa-font"></i> &nbsp;
                        <label class="form-check-label" for="${e}">
                           ${e}
                        </label>
                        <span class="check float-right">
                            <input class="form-check-input" type="checkbox" value="${e}" id="${e}"/>
                        </span>
                    </div>
                </li>`;
  }
  for (e of fields.date) {
    res += `<li class="date-attr ${enabledstr}">
                    <div>
                        <i class="fas fa-calendar-alt"></i> &nbsp;
                        <label class="form-check-label" for="${e}"> ${e} </label>
                        <span class="check float-right">
                            <input class="form-check-input" type="checkbox" value="${e}" id="${e}" />
                        </span>
                    </div>
                </li>`;
  }
  for (e of fields.quant) {
    res += `<li class="quant-attr ${enabledstr}">
                    <div>
                        <i class="fas fa-hashtag"></i> &nbsp;
                        <label class="form-check-label" for="${e}"> ${e} </label>
                        <span class="check float-right">
                            <input class="form-check-input" type="checkbox" value="${e}" id="${e}" />
                        </span>
                    </div>
                </li>`;
  }

  fieldLst.innerHTML += res;
}

function initField(fields) {
  fieldLst.innerHTML = "";
  addFields(fields);

  //adding event listeners to field labels
  let a = document.querySelectorAll("form .enabled div");
  for (i of a) {
    i.addEventListener("click", onClickEvent);
  }

  let modal = document.querySelector("#popup");
  let BMbtn = document.querySelector("#bookmark");
  let closeBtn = document.querySelector(".close");

  // When the user clicks on the button, toggle the modal
  BMbtn.addEventListener("click", () => {
    if (modal.style.display == "block") {
      modal.style.display = "none";
    } else {
      // when the window is displayed, plot charts in divs
      modal.style.display = "block";
      refreshBookmark();
    }
  });
  // When the user clicks on <span> (x), close the modal
  closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });
  // When the user clicks anywhere outside of the modal, close it
  window.addEventListener("click", (event) => {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  });
}

function onClickEvent(e) {
  let box = e.target;
  if (box != null) {
    let s = box.value;
    // if a box is checked after the click
    if (box.checked) {
      // if we can check more fields add the field in.
      // also add its parsed name to the list.
      if (checkedFields.length < 3) {
        checkedFields.push(s);
        // if we can not check more fields, alert it.
      } else {
        alert(`You have selected more than 3 fields!`);
        box.checked = false;
        return;
      }

      // if a box is unchecked after the click,
      // also remove its parsed name from the list.
    } else {
      checkedFields = checkedFields.filter(function (value, index, arr) {
        return value.localeCompare(s) != 0;
      });
      // if 0 fields are checked, display alternative message.
      if (checkedFields.length == 0) {
        mainImg.innerHTML = `Welcome! Start exploring by selecting fields in the Field panel.`;
        return;
      }
    }
    generatePlot(checkedFields, s, box);
  }
}

function refreshBookmark() {
  let arr = bookmarkContent.childNodes;
  let v1keys = [];
  let btnstrs = [];

  if (Object.keys(bookmarked).length == 0) {
    bookmarkContent.innerHTML =
      "Oops, you don't have any bookmark yet. Click on bookmark tags on charts to add a bookmark!";
  } else {
    bookmarkContent.innerHTML = "";
    for (key of Object.keys(bookmarked)) {
      let value = bookmarked[key];
      console.log(bookmarked);
      console.log(key);

      // creat div structure append to the popup window.
      bookmarkContent.innerHTML += `<div class="view_wrapper ${key}_wrapper_bm" ><i class="fas fa-bookmark add_bm" added="true"></i><div class="views cate" id="${key}_bm"></div></div>`;

      // plot the recommandation
      vegaEmbed(`#${key}_bm`, value);

      btnstrs.push(`.${key}_wrapper_bm i`);
      let btn = document.querySelector(`.${key}_wrapper_bm i`);

      // change color and attribute of bookmark.
      btn.style.color = "#ffa500";
      btn.setAttribute("added", "true");
    }
    // add event listener to new bookmark
    for (btn of btnstrs)
      document.querySelector(btn).addEventListener("click", toggleBookMark);
  }
}

function toggleBookMark(e) {
  let btn = e.target;
  let vis = e.target.parentElement;
  let str = vis.classList.item(1);
  // if the mark was checked, user want to uncheck it.
  if (btn.getAttribute("added") == "true") {
    // remove bookmark from pop up window
    let arr = bookmarkContent.childNodes;
    for (n of arr) {
      if (
        `${str}`
          .split("_wrapper")[0]
          .split("_bm")[0]
          .localeCompare(n.classList.item(1).split("_bm")[0]) == 0
      ) {
        bookmarkContent.removeChild(n);
      }
    }
    delete bookmarked[`${str.split("_wrapper")[0]}`];

    // change color and state of the plot in views
    let mark = document.querySelector(`.${str.split("_bm")[0]} i`);
    if (mark != null) {
      mark.style.color = "rgb(216, 212, 223)";
      mark.setAttribute("added", "false");
    }
    refreshBookmark();

    // if the mark is unchecked, user want to check it.
  } else {
    btn.style.color = "#ffa500";
    btn.setAttribute("added", "true");

    let splittedStr = `${str.split("_wrapper")[0]}`;

    bookmarked[splittedStr] = queryMap[splittedStr];
    refreshBookmark();
  }
}

function generatePlot(selectedFields, s, box) {
  console.log(selectedFields);
  var data = {
    data: JSON.stringify({
      fields: selectedFields,
    }),
  };
  $.ajax({
    async: false,
    type: "POST",
    url: "js2pyFieldsv1",
    currentType: "application/json",
    data: data,
    dataType: "json",
    success: function (response) {
      if (response.status === "success") {
        console.log(response);
        var vlDict = response.actualVegaLite;
        for (prop in vlDict) {
          prop_str = prop.replace(/\W/g, "");
          mainImg.innerHTML = `<div id="main_wrapper" class="view_wrapper ${prop_str}_wrapper"><i class="fas fa-bookmark add_bm" added="false"></i><div class="views ${prop_str}" id="main"></div></div>`;
          VlSpec = vlDict[prop];
          vegaEmbed("#main", VlSpec);
          queryMap[prop_str] = VlSpec;
        }

        // add event listeners to all bookmark buttons on the page
        let btns = document.querySelectorAll(".add_bm");
        for (btn of btns) {
          btn.addEventListener("click", toggleBookMark);
        }
        let wrappers = document.querySelectorAll(".view_wrapper");

        // change color and state of a bookmark if a wrapper is in the bookmark content.
        for (wrapper of wrappers) {
          let item = `${wrapper.classList.item(1).split("_wrapper")[0]}`;
          if (item in bookmarked) {
            wrapper.querySelector("i").style.color = "#ffa500";
            wrapper.querySelector("i").setAttribute("added", "true");
          }
        }
      } else if (response.status === "empty") {
        alert(
          "Sorry, we cannot generate charts with the combination of selected fields."
        );
        checkedFields = checkedFields.filter(function (value, index, arr) {
          return value.localeCompare(s) != 0;
        });
        box.checked = false;
      }
    },
  });
}
