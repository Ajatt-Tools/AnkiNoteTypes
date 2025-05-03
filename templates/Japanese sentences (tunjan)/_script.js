(function() {
    'use strict';

    // --- Configuration ---
    const C = {
        EXCL_TAGS: ["tolearn", "marked"], // Tags to exclude from display
        JP1K_TAG: "jp1k", // Tag indicating JP1K mode
        MAX_INLINE_RT: 1, // Max ruby <rt> elements before using tooltip
        KEY_FURIGANA: 'p', // Keybinding to toggle JP1K furigana
        KEY_HINTS: 'a', // Keybinding to reveal hints/translation
        LS_FONT: 'ankiJpFontPreference', // localStorage key for font preference
        FONT_MINCHO: 'mincho',
        FONT_SANS: 'sans',
        CSS_F_MINCHO: 'font-mincho', // Class for Mincho font
        CSS_F_SANS: 'font-sans', // Class for Sans font
        CSS_HIDE: 'is-hidden', // Class to hide elements
        CSS_RT_VIS: 'furigana-rt-visible', // Class to make JP1K furigana visible
        CSS_WRAP_FRONT: 'card-is-front', // Class identifying the front card wrapper
        CSS_WRAP_BACK: 'card-is-back', // Class identifying the back card wrapper
        SEL_TARGET: ".jpsentence b, .jpsentence strong, .target_word", // Elements to apply pitch accent class
        SEL_JP1K_UI: ".jp1k-mode", // Container for JP1K mode elements
        SEL_TSC_UI: ".tsc", // Container for standard (non-JP1K) mode elements
        SEL_JP1K_BTN: ".jp1k-mode .toggle_furigana_button", // Button to toggle JP1K furigana
        SEL_JP1K_RT: ".jp1k-mode ruby rt", // Ruby text elements in JP1K mode
        SEL_HINT: "div.ensentence > a.hint", // Hint link element
        SEL_PITCH_N: "#pitchnum", // Pitch number display element
        SEL_PITCH_P: "#pitchpattern", // Pitch pattern display element
        SEL_FONT_BTN: '#fontToggle', // Font toggle checkbox input
        SEL_WRAP: '.wrap', // Main card wrapper
        SEL_HID_PITCH: "#pitchnum_hidden", // Hidden div for pitch number data
        SEL_HID_KANA: "#kanaword_hidden", // Hidden div for kana data
        SEL_HID_KANJI: "#vocab_kanji_hidden", // Hidden div for kanji data
        SEL_RAW_TAGS_SRC: '#anki-raw-tags', // Hidden div for raw Anki tags
        SEL_TAGS_DISP_CONT: '.tags-container', // Container to display filtered tags
        SEL_AUDIO_MARKED: '.audio-is-marked', // Selector for marked audio containers
        SEL_AUDIO_EL: 'audio', // Audio element itself
    };

    // --- Core Utilities ---
    const $ = (sel, ctx = document) => ctx.querySelector(sel);
    const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
    const getLS = (k, def = null) => localStorage.getItem(k) ?? def;
    const setLS = (k, v) => localStorage.setItem(k, v);
    const getHiddenText = (sel) => $(sel)?.textContent.trim() ?? '';
    const createEl = (tag, { cls, txt, attr } = {}) => {
        const el = document.createElement(tag);
        if (cls) el.className = cls;
        // Ensure textContent is only set if txt is not null/undefined
        if (txt != null) el.textContent = txt;
        if (attr) Object.entries(attr).forEach(([k, v]) => el.setAttribute(k, v));
        return el;
    };

    // --- Services ---
    const Pitch = {
        CLASSES: ['pitch-heiban', 'pitch-atamadaka', 'pitch-odaka', 'pitch-nakadaka'],
        
        getNum(pitchStr) {
            if (!pitchStr) return null;
            const num = parseInt(pitchStr.replace(/[\[\]]/g, ""), 10);
            return isNaN(num) ? null : num;
        },
        
        countMoras(kana) {
            if (!kana) return 0;
            // Remove annotations and normalize
            const morasTxt = kana.replace(/[（(＜<\uff1c].*?[＞)>\uff1e]/g, "").replace(/\s+/g, '').normalize("NFKC");
            if (!morasTxt) return 0;
            
            let count = 0;
            const smallKana = new Set('ゃゅょぁぃぅぇぉャュョァィゥェォ');
            
            for (let i = 0; i < morasTxt.length; i++) {
                if (!smallKana.has(morasTxt[i]) || i === 0 || smallKana.has(morasTxt[i-1])) {
                    count++;
                }
            }
            return count;
        },
        
        isOdaka(num, kana, kanji) {
            if (num === null || num <= 0 || !kana) return false;
            const moras = this.countMoras(kana);
            if (moras === 0) return false;
            
            const isNaAdj = /な$/.test(kanji) && kana.endsWith('な');
            const effectiveMoras = isNaAdj ? moras - 1 : moras;
            
            return effectiveMoras > 0 && effectiveMoras === num;
        },
        
        getClass(num, kana, kanji) {
            if (num === null) return null;
            if (num === 0) return this.CLASSES[0]; // Heiban
            if (num === 1) return this.CLASSES[1]; // Atamadaka
            if (num > 1) {
                return this.isOdaka(num, kana, kanji) ? this.CLASSES[2] : this.CLASSES[3];
            }
            return null;
        },
        
        mark(num, kana, kanji) {
            const accentCls = this.getClass(num, kana, kanji);
            if (!accentCls) return;
            
            const targets = $$(C.SEL_TARGET);
            targets.forEach(word => {
                word.classList.remove(...this.CLASSES);
                word.classList.add(accentCls);
            });
        },
        
        cleanDisplay(kana) {
            const numEl = $(C.SEL_PITCH_N);
            if (numEl) {
                if (numEl.classList.contains('no-pitch-data')) {
                    numEl.remove();
                } else {
                    numEl.textContent = numEl.textContent.replace(/[\[\]]/g, "");
                }
            }

            const pattEl = $(C.SEL_PITCH_P);
            if (pattEl) {
                pattEl.querySelector(`.ajt__pitch_number_tag.no-pitch-data`)?.remove();
                
                if (pattEl.classList.contains('no-pitch-data')) {
                    if (kana) {
                        pattEl.textContent = kana;
                        pattEl.classList.remove('no-pitch-data');
                    } else {
                        pattEl.remove();
                    }
                }
            }
        }
    };

Pitch.getNum = function(pitchStr) {
        if (!pitchStr) return null;
        const num = parseInt(pitchStr.replace(/[\[\]]/g, ""), 10);
        return isNaN(num) ? null : num;
    };
    Pitch.countMoras = function(kana) {
        if (!kana) return 0;
        const morasTxt = kana.replace(/[（(＜<\uff1c].*?[＞)>\uff1e]/g, "").replace(/\s+/g, '').normalize("NFKC");
        if (!morasTxt) return 0;
        let count = 0;
        const smallKana = new Set('ゃゅょぁぃぅぇぉャュョァィゥェォ');
        for (let i = 0; i < morasTxt.length; i++) {
            if (!smallKana.has(morasTxt[i]) || i === 0 || smallKana.has(morasTxt[i-1])) {
                count++;
            }
        }
        return count;
    };
    Pitch.isOdaka = function(num, kana, kanji) {
        if (num === null || num <= 0 || !kana) return false;
        const moras = this.countMoras(kana);
        if (moras === 0) return false;
        const isNaAdj = /な$/.test(kanji) && kana.endsWith('な');
        const effectiveMoras = isNaAdj ? moras - 1 : moras;
        return effectiveMoras > 0 && effectiveMoras === num;
    };
    Pitch.getClass = function(num, kana, kanji) {
        if (num === null) return null;
        if (num === 0) return this.CLASSES[0]; // Heiban
        if (num === 1) return this.CLASSES[1]; // Atamadaka
        if (num > 1) {
            return this.isOdaka(num, kana, kanji) ? this.CLASSES[2] : this.CLASSES[3];
        }
        return null;
    };
    Pitch.mark = function(num, kana, kanji) {
        const accentCls = this.getClass(num, kana, kanji);
        if (!accentCls) return;
        const targets = $$(C.SEL_TARGET);
        targets.forEach(word => {
            word.classList.remove(...this.CLASSES);
            word.classList.add(accentCls);
        });
    };
    Pitch.cleanDisplay = function(kana) {
        const numEl = $(C.SEL_PITCH_N);
        if (numEl) {
            if (numEl.classList.contains('no-pitch-data')) {
                numEl.remove();
            } else {
                numEl.textContent = numEl.textContent.replace(/[\[\]]/g, "");
            }
        }
        const pattEl = $(C.SEL_PITCH_P);
        if (pattEl) {
            pattEl.querySelector(`.ajt__pitch_number_tag.no-pitch-data`)?.remove();
            if (pattEl.classList.contains('no-pitch-data')) {
                if (kana) {
                    pattEl.textContent = kana;
                    pattEl.classList.remove('no-pitch-data');
                } else {
                    pattEl.remove();
                }
            }
        }
    };

    const Furigana = {
        createRuby(kanji, readings) {
            const ruby = createEl('ruby');
            ruby.appendChild(createEl('rb', { txt: kanji }));
            readings.forEach(r => ruby.appendChild(createEl('rt', { txt: r })));
            return ruby;
        },
        
        createTooltip(kanji, readings) {
            const inlineReadings = readings.slice(0, C.MAX_INLINE_RT);
            const tooltipReadings = readings.slice(C.MAX_INLINE_RT);

            const tipContainer = createEl('span', { cls: 'tooltip' });
            tipContainer.appendChild(this.createRuby(kanji, inlineReadings));
            
            if (tooltipReadings.length) {
                const tipTextSpan = createEl('span', { cls: 'tooltip-text' });
                tooltipReadings.forEach(r => 
                    tipTextSpan.appendChild(createEl('span', { cls: 'tooltip-reading', txt: r }))
                );
                tipContainer.appendChild(tipTextSpan);
            }
            
            return tipContainer;
        },
        
        processMultiReadingRuby() {
            $$("ruby:not(ruby ruby)").forEach(ruby => {
                const rb = $("rb", ruby);
                const rt = $("rt", ruby);
                const kanji = rb?.textContent.trim();
                const rawReadings = rt?.textContent.trim();

                if (!kanji || !rawReadings) return;

                // Split readings by common separators
                const readings = rawReadings.split(/[\s;,./／、・。]+/u).filter(Boolean).map(s => s.trim());
                const readingCount = readings.length;

                if (readingCount > C.MAX_INLINE_RT) {
                    ruby.replaceWith(this.createTooltip(kanji, readings));
                } else if (readingCount > 1 || (readingCount === 1 && ruby.querySelectorAll('rt').length > 1)) {
                    ruby.replaceWith(this.createRuby(kanji, readings));
                }
            });
        },
        
        toggleJP1KVisibility() {
            $$(C.SEL_JP1K_RT).forEach(rt => rt.classList.toggle(C.CSS_RT_VIS));
        }
    };

Furigana.createRuby = function(kanji, readings) {
        const ruby = createEl('ruby');
        ruby.appendChild(createEl('rb', { txt: kanji }));
        readings.forEach(r => ruby.appendChild(createEl('rt', { txt: r })));
        return ruby;
    };
    Furigana.createTooltip = function(kanji, readings) {
        const inlineReadings = readings.slice(0, C.MAX_INLINE_RT);
        const tooltipReadings = readings.slice(C.MAX_INLINE_RT);
        const tipContainer = createEl('span', { cls: 'tooltip' });
        tipContainer.appendChild(this.createRuby(kanji, inlineReadings));
        if (tooltipReadings.length) {
            const tipTextSpan = createEl('span', { cls: 'tooltip-text' });
            tooltipReadings.forEach(r =>
                tipTextSpan.appendChild(createEl('span', { cls: 'tooltip-reading', txt: r }))
            );
            tipContainer.appendChild(tipTextSpan);
        }
        return tipContainer;
    };
    Furigana.processMultiReadingRuby = function() {
        $$("ruby:not(ruby ruby)").forEach(ruby => {
            const rb = $("rb", ruby);
            const rt = $("rt", ruby);
            const kanji = rb?.textContent.trim();
            const rawReadings = rt?.textContent.trim();
            if (!kanji || !rawReadings) return;
            const readings = rawReadings.split(/[\s;,./／、・。]+/u).filter(Boolean).map(s => s.trim());
            const readingCount = readings.length;
            if (readingCount > C.MAX_INLINE_RT) {
                ruby.replaceWith(this.createTooltip(kanji, readings));
            } else if (readingCount > 1 || (readingCount === 1 && ruby.querySelectorAll('rt').length > 1)) {
                ruby.replaceWith(this.createRuby(kanji, readings));
            }
        });
    };
    Furigana.toggleJP1KVisibility = function() {
        $$(C.SEL_JP1K_RT).forEach(rt => rt.classList.toggle(C.CSS_RT_VIS));
    };

    const Font = {
        apply(useMincho) {
            const wrap = $(C.SEL_WRAP);
            if (!wrap) return;
            
            wrap.classList.toggle(C.CSS_F_MINCHO, useMincho);
            wrap.classList.toggle(C.CSS_F_SANS, !useMincho);
            setLS(C.LS_FONT, useMincho ? C.FONT_MINCHO : C.FONT_SANS);
        },
        
        init() {
            const useMincho = getLS(C.LS_FONT) === C.FONT_MINCHO;
            this.apply(useMincho);

            const btn = $(C.SEL_FONT_BTN);
            if (btn && btn.type === 'checkbox') {
                btn.checked = useMincho;
                btn.addEventListener('change', e => this.apply(e.target.checked));
            }
        }
    };

Font.apply = function(useMincho) {
        const wrap = $(C.SEL_WRAP);
        if (!wrap) return;
        wrap.classList.toggle(C.CSS_F_MINCHO, useMincho);
        wrap.classList.toggle(C.CSS_F_SANS, !useMincho);
        setLS(C.LS_FONT, useMincho ? C.FONT_MINCHO : C.FONT_SANS);
    };
    Font.init = function() {
        const useMincho = getLS(C.LS_FONT) === C.FONT_MINCHO;
        this.apply(useMincho);
        const btn = $(C.SEL_FONT_BTN);
        if (btn && btn.type === 'checkbox') {
            btn.checked = useMincho;
            btn.addEventListener('change', e => this.apply(e.target.checked));
        }
    };

    // --- Tag Processing ---
    const processTags = () => {
        const rawTagsSrcEl = $(C.SEL_RAW_TAGS_SRC);
        const tagsDisplayCont = $(C.SEL_TAGS_DISP_CONT);
        // Ensure both required elements exist before proceeding
        if (!rawTagsSrcEl || !tagsDisplayCont) {
            tagsDisplayCont?.classList.add(C.CSS_HIDE); // Hide container if source missing
            return false; // Indicate JP1K status cannot be determined
        }

        const rawTags = rawTagsSrcEl.textContent.trim();
        const allTags = rawTags ? rawTags.split(/\s+/).filter(Boolean).map(t => t.toLowerCase()) : [];
        const isJP1K = allTags.includes(C.JP1K_TAG);

        // Filter and display tags
        const displayTags = allTags.filter(tag => !C.EXCL_TAGS.includes(tag));

        // Use replaceChildren for modern/cleaner clearing and appending
        if (displayTags.length) {
            const fragment = document.createDocumentFragment();
            displayTags.forEach(tag => fragment.appendChild(createEl('div', { cls: 'tags', txt: tag })));
            tagsDisplayCont.replaceChildren(fragment); // Clears and adds in one step
            tagsDisplayCont.classList.remove(C.CSS_HIDE);
        } else {
            tagsDisplayCont.replaceChildren(); // Clear content
            tagsDisplayCont.classList.add(C.CSS_HIDE);
        }

        return isJP1K;
    };

    // --- Event Handling ---
     const setupKeybindings = () => {
        document.addEventListener("keydown", e => {
            // Ignore keydowns in input fields or contenteditable elements
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable) {
                return;
            }

            const key = e.key?.toLowerCase();
            if (!key) return;

            // Toggle JP1K Furigana ('p')
            if (key === C.KEY_FURIGANA) {
                // Check if the JP1K UI *itself* is visible, not just the button within it
                const jp1kUI = $(C.SEL_JP1K_UI);
                if (jp1kUI && jp1kUI.offsetParent !== null) { // Check if UI container is rendered
                    Furigana.toggleJP1KVisibility();
                    e.preventDefault();
                }
            // Reveal Hints/Translation ('a')
            } else if (key === C.KEY_HINTS) {
                 // Check if we are likely on the back card by looking for core back-card content
                 const isLikelyBack = $(C.SEL_WRAP)?.classList.contains(C.CSS_WRAP_BACK);
                 if (isLikelyBack) {
                    // Find visible hint links specifically
                    const visibleHints = $$(C.SEL_HINT).filter(hint => hint.offsetParent !== null);
                    if (visibleHints.length) {
                        visibleHints.forEach(hint => hint.click());
                        e.preventDefault();
                    }
                 }
            }
        });
    };


    // --- Initialization ---
    const init = () => {
        try {
            const wrapElement = $(C.SEL_WRAP);
            if (!wrapElement) {
                console.warn("AnkiJP Card Error: '.wrap' element not found. Cannot initialize.");
                return;
            }

            const isJP1K = processTags();
            Font.init();
            Furigana.processMultiReadingRuby(); // Process complex ruby on both sides if needed
            setupKeybindings();

            // *** Determine card side using the reliable class on the wrapper ***
            const isFront = wrapElement.classList.contains(C.CSS_WRAP_FRONT);
            const isBack = wrapElement.classList.contains(C.CSS_WRAP_BACK);

            // --- Front Card Logic ---
            if (isFront) {
                // Toggle visibility based on JP1K tag
                $$(C.SEL_JP1K_UI, wrapElement).forEach(el => el.classList.toggle(C.CSS_HIDE, !isJP1K));
                $$(C.SEL_TSC_UI, wrapElement).forEach(el => el.classList.toggle(C.CSS_HIDE, isJP1K));

                // Add button listener only if JP1K mode is active
                if (isJP1K) {
                    const jp1kButton = $(C.SEL_JP1K_BTN, wrapElement);
                    jp1kButton?.addEventListener('click', e => {
                        Furigana.toggleJP1KVisibility();
                        e.preventDefault(); // Prevent potential form submission/navigation
                    });
                }
            }

            // --- Back Card Logic ---
            if (isBack) {
                // Process pitch data (only relevant on the back)
                const pitchStr = getHiddenText(C.SEL_HID_PITCH);
                if (pitchStr) {
                    const kana = getHiddenText(C.SEL_HID_KANA);
                    const kanji = getHiddenText(C.SEL_HID_KANJI);
                    const pitchNum = Pitch.getNum(pitchStr);

                    Pitch.mark(pitchNum, kana, kanji);
                    Pitch.cleanDisplay(kana);
                }

                // Update hint link text (if present)
                const hintLink = $(C.SEL_HINT, wrapElement);
                if (hintLink) hintLink.textContent = "Reveal English translation";

                // Handle marked audio elements (hide controls, add class)
                $$(C.SEL_AUDIO_MARKED, wrapElement).forEach(audioDiv => {
                    audioDiv.classList.add('audio-hidden'); // Add visual hiding class (ensure CSS defines this)
                    $(C.SEL_AUDIO_EL, audioDiv)?.removeAttribute('controls');
                });
            }

        } catch (error) {
            console.error("AnkiJP Card Error:", error);
            // Optionally display an error message on the card itself for easier debugging
            // const errorDiv = createEl('div', { txt: `JS Error: ${error.message}`, style: 'color: red; font-size: small;'});
            // document.body.prepend(errorDiv);
        }
    };

    // Run initialization script once the DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // DOM is already loaded
        init();
    }
})();