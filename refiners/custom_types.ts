import { LargeNumberLike } from "crypto";

// COURSES
export type Courses = Record<string, Course>;
export type ScrapedCourses = Record<string, ScrapedCourse>;
export type ScrapedCourse = Partial<Course>;
export type Course = {
  name: string;
  uoc: string;
  overview: string;
  prereqs: string;
  equivalent_courses: string[];
  exclusion_courses: string[];
  is_gen_ed: boolean;
  is_intro: boolean;
  is_multi_term: boolean;
  faculty: string;
  school: string;
  study_level: string;
  offering_terms: string;
  campus: string;
  academic_calendar: string;
  field_of_education: string;
};

export type ProcessedCourses = Record<string, ProcessedCourse>;
export type ProcessedCourse = {
  name: string;
  uoc: number;
  overview: string;
  subject: string;
  level: number;
  school: string;
  terms_available: string[];
  equivalent_courses: string[];
  exclusion_courses: string[]; 
  unlocked_by: string[];
  unlocks: string[];
  other_requirements: {
    uoc?: number;
    wam?: number;
    subject?: string;
    level?: number;
    programs?: number[];
    specialisation?: string;
    corequisites?: string[];
    all_found_courses?: string[];
    course_group_bool?: string;
    raw_str?: string;
  };
  is_intro: boolean;
  is_gen_ed: boolean;
  is_multi_term: boolean;
};


export type Subjects = Record<string, Subject>;
export type Subject = {
  code: string;
  name: string;
  courses: string[];
};

export type Schools = Record<string, School>;
export type School = {
  subjects: string[];
};

export type Faculties = Record<string, Faculty>;
export type Faculty = {
  name: string;
  overview: string;
  Programs?: string[];
  'Double Degrees'?: string[];
  Specialisations?: {
    Major?: string[];
    Minor?: string[];
    Honours?: string[];
  };
  schools?: string[];
};