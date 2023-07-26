<!--
mpvacious cards, version 15.0
Fri Jul  7 06:33:50 PM UTC 2023
-->

<div class="wrap">
    <header>
        {{#Focus}}
        <div class="tags">{{Focus}}</div>
        {{/Focus}}
        {{#Tags}}
        <div class="tags">{{Tags}}</div>
        {{/Tags}}
    </header>

    <div class="sent-center">
        <div class="jpsentence" lang="ja">
            {{edit:furigana:SentKanji}}
            {{^SentKanji}}
            <nokana>{{edit:kanji:SentFurigana}}</nokana>
            {{/SentKanji}}
        </div>
    </div>

    {{#Image}}
    <details class="images-on-front images-details">
        <summary>Image</summary>
        <div class="images">{{Image}}</div>
    </details>
    {{/Image}}
</div> <!-- /wrap -->

<div style="display:none;">
    <div id="pitchnum_hidden">{{VocabPitchNum}}</div>
    <div id="kanaword_hidden">{{kana:VocabFurigana}}</div>
</div>

<script>
    /* Paints the question word according to its Pitch Accent number.
     * blue for 平板
     * red for 頭高
     * orange for 中高
     * green for 尾高
     */
    function markPitch() {
        let pitchNumber = document.getElementById("pitchnum_hidden");
        if (pitchNumber === null) {
            return;
        } else {
            pitchNumber = pitchNumber.innerHTML.match(/\d/);
        }
        if (pitchNumber === null) {
            return;
        } else {
            pitchNumber = Number(pitchNumber);
        }

        /* Then decide what color to use and change font color accordingly. */
        if (pitchNumber == 0) {
            // use blue for 平板
            paintTargetWord("#3366CC");
        } else if (pitchNumber == 1) {
            // use red for 頭高
            paintTargetWord("red");
        } else if (pitchNumber > 1) {
            if (odaka(pitchNumber)) {
                // use green for 尾高
                paintTargetWord("green");
            } else {
                // use orange for 中高
                paintTargetWord("#ff6207");
            }
        }
    }

    function paintTargetWord(color) {
        for (const word of document.querySelectorAll(".jpsentence b, .jpsentence strong")) {
            word.style.color = color;
        }
    }

    function odaka(pitch_num) {
        // word is odaka if number of moras is equal to pitch accent position
        const vocab_kana = document.getElementById("kanaword_hidden");
        if (vocab_kana === null) {
            return false;
        }
        // small っ is one mora; ゃゅょ are parts of single mora
        const n_moras = vocab_kana.innerHTML.replace(/[ャュョゃゅょ]/g, "").length;
        if (n_moras == pitch_num) {
            return true;
        } else {
            return false;
        }
    }

    /* Splits tags into separate divs */
    function splitTagDiv() {
        const header = document.querySelector("header");
        if (!header) return;
        const split = `{{Focus}} {{Tags}}`.split(" ");
        const dont_show = ['imageonfront', 'tolearn', 'marked',];

        header.innerHTML = "";

        for (const tag of split) {
            if (tag.length < 1 || dont_show.includes(tag)) continue;
            const tag_elem = document.createElement("div");
            tag_elem.className = "tags";
            tag_elem.innerText = tag;
            header.appendChild(tag_elem);
        }
    }

    function formatNewRuby(kanji, readings) {
        if (readings.length > 1) {
            return `<ruby>${formatNewRuby(kanji, readings.slice(0, -1))}</ruby><rt>${readings.slice(-1)}</rt>`
        } else {
            return `<rb>${kanji}</rb><rt>${readings.join('')}</rt>`
        }
    }

    function reformatMultiFurigana() {
        const separators = /[\s;,.、・。]+/iu;
        const max_inline = 2;
        document.querySelectorAll("ruby:not(ruby ruby)").forEach(ruby => {
            try {
                const kanji = (ruby.querySelector("rb") || ruby.firstChild).textContent.trim();
                const readings = ruby.querySelector("rt").textContent
                    .split(separators)
                    .map(str => str.trim())
                    .filter(str => str.length);

                if (readings.length > 1) {
                    ruby.innerHTML = formatNewRuby(kanji, readings.slice(0, max_inline));
                }
                if (readings.length > max_inline) {
                    const sequence = readings.map(reading => `<span class="tooltip-reading">${reading}</span>`).join('');
                    const wrapper = document.createElement("span");
                    wrapper.classList.add("tooltip");
                    wrapper.innerHTML += `<span class="tooltip-text">${sequence}</span>`;
                    ruby.replaceWith(wrapper);
                    wrapper.appendChild(ruby);
                }
            } catch (error) {
                console.error(error);
            }
        })
    }

    function isMobile() {
        return document
            .getElementsByTagName("html")[0]
            .classList
            .contains("mobile");
    }

    /* If a card has the "imageonfront" tag set, show images on the front side. */
    function setVisibleImageOnFront() {
        if (`{{Tags}}`.split(" ").includes("imageonfront")) {
            for (const frontImg of document.querySelectorAll(".images-on-front")) {
                frontImg.setAttribute("visible", true);
            }
        }
    }

    /* Hide images on mobile devices. */
    function toggleImageDetails() {
        for (const detailsElement of document.querySelectorAll(".images-details")) {
            detailsElement.toggleAttribute("open", !isMobile());
        }
    }

    markPitch();
    splitTagDiv();
    reformatMultiFurigana();
    setVisibleImageOnFront();
    toggleImageDetails();
</script>
