import questions from "./questions.json";

import { action, makeObservable, observable } from "mobx";

 

const { decisions } = questions;

 

type LikertAnswer = {

  id: number;

  value: number;

  text?: string;

  leaf: boolean;

  options?: number[];

};

 

class BehavioralQuestions {

  answers: LikertAnswer[] = [];

  historyIndex = -1;

  currentQuestions?: LikertAnswer[] | null = null;

  currentCareer?: number | null = null;

 

  startQuestions = () => {

    this.historyIndex = 0;

  };

 

  calculateNext = () => {

    this.historyIndex++;

    this.calculateCurrent();

  };

 

  calculatePrevious = () => {

    this.historyIndex--;

    this.calculateCurrent();

  };

 

  buildItem(id: number) {

    const existing = this.answers.find((a) => a.id === id);

    if (existing) {

      return existing;

    }

    const decision = decisions.find((de) => de.id === id);

    if (decision == null) {

      throw new Error(`Decision ${id} not found`);

    }

    const result = observable({

      id: id,

      value: -1,

      text: decision.text,

      options: decision.true,

      leaf: !decision.true, // it does not have true values

    });

    this.answers.push(result);

    return result;

  }

 

  buildItems(ids: number[]) {

    return ids.map((id) => this.buildItem(id));

  }

 

 

  createInitialQueue() {

    const decision = decisions.find((d) => d.id === 0);

    if (decision?.true == null) {

      throw new Error("There must be initial decision point");

    }

    return this.buildItems(decision.true);

  }

 

 

  /**

   * Calculates next step and either returns the three questions to ask, or a job selection

   * The algorithm processes the whole queue from the start and always groups the questions by

   * threes. Then, for each answered question:

   * 1. adds the other options to the end of the queue, if answer was MAYBE

   * 2. adds right after if the answer was yes

   * 3. Depending on whether “this.currentQuestions” or “this.currentCareer” is selected we render

   *    either a list of three questions or a list of potential career choices. The other must always be null

   * 4. The leaf nodes provide “career” choices relating to the ANZSCO code

   */

  private calculateCurrent(): void {

    // if we are starting, just take the first three root questions

    if (this.answers.length === 0 || this.historyIndex === 0) {

      const initialQueue = this.createInitialQueue();

      if (initialQueue != null) {

        this.currentQuestions = initialQueue.slice(0, 3);

        this.currentCareer = null;

      }

 

      return;

    }

 

    // now browse through all the answers and generate a chain stopping at the desired index

    // take them in group of threes and calculate a next step

    let index = 0;

    let page = 0;

    const generatedQueue: Array<LikertAnswer | number> =

      this.createInitialQueue();

    let threeQuestions: LikertAnswer[] = [];

 

    while (index < generatedQueue.length) {

      // check if the next is a career page or a question

      // question is an object, career is a number

      const nextElement = generatedQueue[index];

      index++;

 

      // this is a career page

      if (typeof nextElement === "number") {

        if (page === this.historyIndex) {

          this.currentCareer = nextElement;

          this.currentQuestions = null;

 

          return;

        } else {

          page++;

          continue;

        }

      }

      // this is a question

      else if (nextElement != null) {

        threeQuestions.push(nextElement);

      } else {

        throw new Error("Invalid element");

      }

 

      // we must have three questions per page or we are at the end of the queue

      if (threeQuestions.length < 3 && index < generatedQueue.length) {

        continue;

      }

 

      // we filled the three questions process them in the queue

      // first check if we can finish

      if (page === this.historyIndex) {

        this.currentQuestions = threeQuestions;

        this.currentCareer = null;

 

        return;

      }

      page++;

 

      // if not we process the answers in the current question set

      // and add them either at the end of the queue for MAYBE options

      // or right after if it a YES option

 

      for (const answer of threeQuestions) {

        if (answer.value === 1) {

          // this is a MAYBE answer, we add it to the end of the queue

          if (answer.leaf) {

            generatedQueue.push(answer.id);

          } else if (answer.options) {

            generatedQueue.push(...this.buildItems(answer.options));

          }

        } else if (answer.value === 2) {

          // this is a YES answer, we add it as a next option

          if (answer.leaf) {

            generatedQueue.splice(index, 0, answer.id);

          } else if (answer.options) {

            generatedQueue.splice(index, 0, ...this.buildItems(answer.options));

          }

        }

      }

 

      threeQuestions = [];

    }

 

    this.currentQuestions = [];

    this.currentCareer = null;

  }

}