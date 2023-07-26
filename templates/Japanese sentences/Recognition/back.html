<div class="wrap">
    <div class="fside">{{FrontSide}}</div>

    <div class="sent-center">
        <div class="jpsentence" lang="ja">
            <div class="background">{{furigana:SentFurigana}}{{^SentFurigana}}{{furigana:SentKanji}}{{/SentFurigana}}</div>
            <div class="overlay">{{edit:furigana:SentFurigana}}{{^SentFurigana}}{{edit:furigana:SentKanji}}{{/SentFurigana}}</div>
        </div>
        {{#SentEng}}
        <div class="ensentence" lang="en">{{hint:SentEng}}</div>
        {{/SentEng}}
    </div>

    {{#VocabDef}}
    <section class="headword_section">
        <div class="vocab">
            <span id="vocab-audio">{{VocabAudio}}</span>
            <span id="sent-audio">{{SentAudio}}</span>
            <div class="reading" id="pitchpattern">{{VocabPitchPattern}}{{^VocabPitchPattern}}{{text:kana:VocabFurigana}}{{/VocabPitchPattern}}</div>
            {{#VocabPitchNum}}<span class="tags" id="pitchnum">{{text:VocabPitchNum}}</span>{{/VocabPitchNum}}
            {{#VocabKanji}}<div class="target_word">{{text:kanji:VocabKanji}}</div>{{/VocabKanji}}
        </div>
        <div class="definitions">{{edit:furigana:VocabDef}}</div>
    </section>
    {{/VocabDef}}

    {{#Notes}}
    <details open class="notes">
        <summary>Notes</summary>
        <div>{{furigana:Notes}}</div>
    </details>
    {{/Notes}}

    {{#Image}}
    <details class="images-details">
        <summary>Image</summary>
        <div class="images">{{Image}}</div>
    </details>
    {{/Image}}

    <hr>

    <footer>
        {{#SentKanji}}
        <a href="https://simplytranslate.org/?engine=google&text={{text:kanji:SentKanji}}&sl=ja&tl=en" title="Translate with SimplyTranslate">Translate</a>
        <a href="https://jisho.org/search?keyword={{text:kanji:SentKanji}}" title="Sentence on Jisho">Jisho</a>
        <a href="https://www.google.co.jp/search?q={{text:kanji:SentKanji}}&tbm=isch" title="Search images">Images</a>
        {{/SentKanji}}
        {{#VocabKanji}}
        <a href="http://www.weblio.jp/content/{{text:VocabKanji}}" title="Vocab on Weblio">Weblio</a>
        <a href="https://wadoku.de/search/?q={{text:VocabKanji}}" title="Vocab on Wadoku">Wadoku</a>
        {{/VocabKanji}}
    </footer>
</div> <!-- /wrap -->

<script>
    function tweakRevealText() {
        const elem = document.querySelector("div.ensentence > a.hint");
        if (elem) {
            elem.innerText = "Reveal English translation";
        }
    }

    function removePitchBrackets() {
        const tags = document.getElementById("pitchnum");
        if (tags !== null) {
            tags.innerHTML = tags.innerHTML.replace(/[\[\]]/g, "");
        }
    }

    function removeNoPitchAccentDataText() {
        const has_no_data = (tag) => tag.innerText.toLowerCase().includes("no pitch accent");
        const pitch_num = document.getElementById("pitchnum");
        const pitch_pattern = document.getElementById("pitchpattern");
        const pitch_num_inside_html = document.querySelector(".pitch_number");
        if (pitch_num && has_no_data(pitch_num)) {
            pitch_num.remove();
        }
        if (pitch_pattern && has_no_data(pitch_pattern)) {
            pitch_pattern.innerHTML = `{{text:kana:VocabFurigana}}`;
        }
        if (pitch_num && pitch_num_inside_html) {
            pitch_num.remove();
        }
    }

    function removeAudioIfMarkedX() {
        const pr = document.getElementById("vocab-audio");
        if (pr && pr.innerText.match(/^[x×]/i)) {
            pr.style.display = "none";
        }
    }

    markPitch();
    removePitchBrackets();
    tweakRevealText();
    removeNoPitchAccentDataText();
    reformatMultiFurigana();
    removeAudioIfMarkedX();
    toggleImageDetails();
</script>
