import dataUtil from 'src/utils/data.js'

export const SECTION_TYPES = {
  TEXT: {
    key: 'TEXT',
    label: 'Text section',
    sectionPartConfig: { html_content: '' },
    usedFor: ['About us', 'Why work for us', 'Diversity & Inclusion']
  },
  ICON: {
    key: 'ICON',
    label: 'Icons section',
    sectionPartConfig: { header: null, html_content: '', icon: null },
    usedFor: ['Benefits', 'Values', 'Hiring process'],
    exampleImagePath: '/images/iconsSectionExample.png'
  },
  CAROUSEL: {
    key: 'CAROUSEL',
    label: 'Picture carousel section',
    sectionPartConfig: { header: null, picture_ids: [], is_allow_autoplay: false },
    usedFor: ['Company culture', 'Faces of employees'],
    exampleImagePath: '/images/carouselSectionExample.png'
  },
  ACCORDION: {
    key: 'ACCORDION',
    label: 'Accordion list section',
    sectionConfig: { accordion_header_color: null, accordion_background_color: null },
    sectionPartConfig: { header: null, html_content: '' },
    usedFor: ['FAQ'],
    exampleImagePath: '/images/accordionSectionExample.png'
  }
}

class SectionUtil {
  /**
   * Add a new section configuration to a list of sections
   * @param sections {Array}: A list of current sections
   * @param sectionType {String}: A section type key
   */
  addSectionItem (sections, sectionType) {
    const extraConfig = SECTION_TYPES[sectionType].sectionConfig || {}
    sections.push({
      type: sectionType,
      header: null,
      config: {
        background_color: null,
        header_color: null,
        text_color: null,
        ...extraConfig
      },
      item_parts: [
        dataUtil.deepCopy(SECTION_TYPES[sectionType].sectionPartConfig)
      ]
    })
  }
}

const sectionUtil = new SectionUtil()

export default sectionUtil
