var dataurl = "data/movies.json";
var Fields = {
  categ: [
    "Creative_Type",
    "Director",
    "Distributor",
    "Major_Genre",
    "MPAA_Rating",
    "Source",
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
var relatedImg = document.querySelector(".relatedImg");

// names of selected field
var checkedFields = [];
var queryMap = {};
var bookmarked = {};

// document.querySelector("#main_wrapper").style.display = "none";
//d3.json(dataurl).then(initial);
initial();

function initial() {
  //myData = data;
  initField(Fields);
}

function addFields(fields) {
  let res = "";
  let disabledstr = "";
  let enabledstr = "enabled";
  for (e of fields.categ) {
    res += `<li class="categ-attr ${enabledstr} ${disabledstr}">
                    <div>
                        <i class="fas fa-font"></i> &nbsp;
                        <label class="form-check-label" for="${e}">
                           ${e}
                        </label>
                        <span class="check float-right">
                            <input class="form-check-input" type="checkbox" value="${e}" id="${e}" ${disabledstr}/>
                        </span>
                    </div>
                </li>`;
  }
  for (e of fields.date) {
    res += `<li class="date-attr ${enabledstr} ${disabledstr}">
                    <div>
                        <i class="fas fa-calendar-alt"></i> &nbsp;
                        <label class="form-check-label" for="${e}"> ${e} </label>
                        <span class="check float-right">
                            <input class="form-check-input" type="checkbox" value="${e}" id="${e}" ${disabledstr} />
                        </span>
                    </div>
                </li>`;
  }
  for (e of fields.quant) {
    res += `<li class="quant-attr ${enabledstr} ${disabledstr}">
                    <div>
                        <i class="fas fa-hashtag"></i> &nbsp;
                        <label class="form-check-label" for="${e}"> ${e} </label>
                        <span class="check float-right">
                            <input class="form-check-input" type="checkbox" value="${e}" id="${e}" ${disabledstr} />
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
    let s = box.value.split(" ").join("_");
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
        mainImg.innerHTML = ` Welcome! Please select fields to generate recommanded charts.`;
        return;
      }
    }
  }
  let fieldStr = "";
  for (s of checkedFields) {
    fieldStr += s + "-";
  }
  fieldStr = fieldStr.substring(0, fieldStr.length - 1);

  mainImg.innerHTML = `<div id="main_wrapper" class="view_wrapper ${fieldStr}_wrapper"><i class="fas fa-bookmark add_bm" added="false"></i><div class="views ${fieldStr}" id="main"></div></div>`;
  generatePlot(checkedFields, fieldStr);

  // add event listeners to all bookmark buttons on the page
  let btns = document.querySelectorAll(".add_bm");
  for (btn of btns) {
    btn.addEventListener("click", toggleBookMark);
  }
  // change color and state of a bookmark if a wrapper is in the bookmark content.
  let wrappers = document.querySelectorAll(".view_wrapper");

  for (wrapper of wrappers) {
    let item = `v2_${wrapper.classList.item(1).split("_wrapper")[0]}`;
    if (item in bookmarked) {
      wrapper.querySelector("i").style.color = "#60608A";
      wrapper.querySelector("i").setAttribute("added", "true");
      // console.log(wrapper.classList.item(1).split("_bm")[0] + " exists!! " + btn.style.color);
    }
  }
}

function refreshBookmark() {
  let arr = bookmarkContent.childNodes;
  let v2keys = [];
  let btnstrs = [];
  for (var key in bookmarked) {
    if (key.startsWith("v2_")) v2keys.push(key);
  }

  if (v2keys.length == 0) {
    bookmarkContent.innerHTML =
      "Oops, you don't have any bookmark yet. Click on bookmark tags on charts to add a bookmark!";
  } else {
    bookmarkContent.innerHTML = "";
    for (key of v2keys) {
      let k = key.substring(3);
      let value = bookmarked[key];
      console.log(value);

      // creat div structure append to the popup window.
      bookmarkContent.innerHTML += `<div class="view_wrapper ${k}_wrapper_bm" ><i class="fas fa-bookmark add_bm" added="true"></i><div class="views cate" id="${k}_bm"></div></div>`;

      // plot the recommandation
      vegaEmbed(`#${k}_bm`, value);

      btnstrs.push(`.${k}_wrapper_bm i`);
      let btn = document.querySelector(`.${k}_wrapper_bm i`);

      // change color and attribute of bookmark.
      btn.style.color = "#60608A";
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
    delete bookmarked[`v2_${str.split("_wrapper")[0]}`];

    // change color and state of the plot in views
    let mark = document.querySelector(`.${str.split("_bm")[0]} i`);
    if (mark != null) {
      mark.style.color = "rgb(216, 212, 223)";
      mark.setAttribute("added", "false");
    }
    refreshBookmark();

    // if the mark is unchecked, user want to check it.
  } else {
    btn.style.color = "#60608A";
    btn.setAttribute("added", "true");

    let splittedStr = `v2_${str.split("_wrapper")[0]}`;

    // if there is currently no charts, empty its inner html.
    // if (Object.keys(bookmarked).length == 0) {
    //     bookmarkContent.innerHTML = "";
    // }

    bookmarked[splittedStr] = queryMap[splittedStr.substring(3)];
    refreshBookmark();
  }
}

function generatePlot(arr, str) {
  console.log(arr);
  var data = {
    data: JSON.stringify({
      fields: arr,
    }),
  };
  $.ajax({
    async: false,
    type: "POST",
    url: "js2pyFieldsv3",
    currentType: "application/json",
    data: data,
    dataType: "json",
    success: function (response) {
      console.log(response);
      var VlSpec = response.actualVegaLite;
      queryMap[str] = VlSpec;
      vegaEmbed("#main", VlSpec);
      var recVlSpec = response.recVegaLite;
      relatedImg.innerHTML = "";
      generateRecPlot(recVlSpec);
    },
  });
}

function generateRecPlot(recVlSpec) {
  relatedImg.innerHTML = "";
  for (var i = 0; i < 5; i++) {
    let queryClassName = JSON.stringify(recVlSpec[i]).replace(/\W/g, "");
    relatedImg.innerHTML += `<div class='view_wrapper ${queryClassName}_wrapper'><i class='fas fa-bookmark add_bm' added="false"></i><div class="views cate" id='${queryClassName}'></div></div>`;
    vegaEmbed(`#${queryClassName}`, recVlSpec[i]);
  }
}
