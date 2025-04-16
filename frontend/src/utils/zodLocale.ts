// src/utils/zodLocale.ts
import type { ZodErrorMap } from 'zod';
import { z, ZodIssueCode } from 'zod';

export const errorMap: ZodErrorMap = (issue, _ctx) => {
  // console.log(issue)
  switch (issue.code) {
    case ZodIssueCode.invalid_type:
      if (issue.received === 'undefined') {
        return { message: 'Không được để trống' };
      }
      return { message: `Kiểu dữ liệu không hợp lệ. Mong đợi ${issue.expected}, nhận được ${issue.received}` };
    case ZodIssueCode.invalid_string:
      if (issue.validation === 'email') {
        return { message: 'Địa chỉ email không hợp lệ' };
      }
      if (issue.validation === 'url') {
        return { message: 'URL không hợp lệ' };
      }
      return { message: 'Chuỗi không hợp lệ' };
    case ZodIssueCode.too_small:
      return { message: `Giá trị phải lớn hơn hoặc bằng ${issue.minimum}` };
    case ZodIssueCode.too_big:
      return { message: `Giá trị phải nhỏ hơn hoặc bằng ${issue.maximum}` };
    default:
      return { message: 'Giá trị không hợp lệ' };
  }
};

z.setErrorMap(errorMap);
