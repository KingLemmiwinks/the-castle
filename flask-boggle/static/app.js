// Make Boggle Game
class BoggleGame {
  constructor(boardId, secs = 60) {
    this.secs = secs; // Game Timer
    this.showTimer(); // Show Game Timer

    this.score = 0; // Current Score
    this.words = new Set();
    this.board = $("#" + boardId);
    this.timer = setInterval(this.tick.bind(this), 1000); // Tick every second (1000ms)

    $("#add-word", this.board).on("submit", this.handleSubmit.bind(this));
  }

  // Show word in list
  showWord(word) {
    $("#words", this.board).append($("<li>", { text: word }));
  }

  // Show Score on page
  showScore() {
    $("#score", this.board).text(this.score);
  }

  // Show status message when triggered
  showMessage(msg, cls) {
    $("#msg", this.board).text(msg).removeClass().addClass(`msg ${cls}`);
  }

  // Handle word submit
  // Check to see if word is valid
  // If not, show error message
  // If so, show word and add word length to score
  async handleSubmit(evt) {
    evt.preventDefault();
    const $word = $("#word", this.board);

    let word = $word.val();
    if (!word) return;

    if (this.words.has(word)) {
      this.showMessage(`Already found ${word}`, "err");
      return;
    }

    const resp = await axios.get("/check-word", { params: { word: word } });
    if (resp.data.result === "not-word") {
      this.showMessage(`${word} is not a valid English word`, "err");
    } else if (resp.data.result === "not-on-board") {
      this.showMessage(`${word} is not a valid word on this board`, "err");
    } else {
      this.showWord(word);
      this.score += word.length;
      this.showScore();
      this.words.add(word);
      this.showMessage(`Added: ${word}`, "ok");
    }
    $word.val("").focus();
  }

  // Show timer on page
  showTimer() {
    $("#timer", this.board).text(this.secs);
  }

  // Handles passing seconds
  async tick() {
    this.secs -= 1;
    this.showTimer();

    if (this.secs === 0) {
      clearInterval(this.timer);
      await this.scoreGame();
    }
  }

  // Shows score and update message at endgame
  async scoreGame() {
    $("#add-word", this.board).hide();
    const resp = await axios.post("/post-score", { score: this.score });
    if (resp.data.brokeRecord) {
      this.showMessage(`New record: ${this.score}`, "ok");
    } else {
      this.showMessage(`Final score: ${this.score}`, "ok");
    }
  }
}
