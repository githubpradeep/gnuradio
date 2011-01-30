#ifndef INCLUDED_QA_32F_CALC_SPECTRAL_NOISE_FLOOR_ALIGNED16_H
#define INCLUDED_QA_32F_CALC_SPECTRAL_NOISE_FLOOR_ALIGNED16_H

#include <cppunit/extensions/HelperMacros.h>
#include <cppunit/TestCase.h>

class qa_32f_calc_spectral_noise_floor_aligned16 : public CppUnit::TestCase {

  CPPUNIT_TEST_SUITE (qa_32f_calc_spectral_noise_floor_aligned16);
  CPPUNIT_TEST (t1);
  CPPUNIT_TEST_SUITE_END ();

 private:
  void t1 ();
};


#endif /* INCLUDED_QA_32F_CALC_SPECTRAL_NOISE_FLOOR_ALIGNED16_H */
