<template>
  <div v-if="isLoaded" class="q-gutter-y-md">
    <CollapsableCard title="Post filters" :is-dense="true">
      <template v-slot:body>
        <div class="col-12 q-pa-sm">
          <div class="row q-gutter-y-sm">
            <div class="col-12 col-md-6 q-pr-md-sm">
              <SelectPlatform v-model="postFilter.platforms" :is-multi="true"/>
            </div>
            <div class="col-12 col-md-6 q-pl-md-sm">
              <DateRangeSelector v-model="postFilter.dateRange" placeholder="Post date"/>
            </div>
            <div v-if="isEmployees" class="col-12 col-md-6 q-pr-md-sm">
              <SelectEmployee v-model="postFilter.employee_ids" :employer-id="user.employer_id"/>
            </div>
          </div>
        </div>
      </template>
    </CollapsableCard>
    <q-card v-if="!socialPosts || !socialPosts.length" class="q-pa-md text-bold text-grey-6">
      No posts to display
    </q-card>
    <div class="row q-gutter-y-md">
      <div v-for="post in socialPosts" class="col-12 col-md-6 q-px-sm h-100">
        <CollapsableCard class="h-100" :can-collapse="false">
          <template v-slot:header-left>
            <img :src="post.platform.logo" alt="Social platform logo" style="max-height: 32px">
            <div class="row q-ml-md">
              <div class="col-12">
                <div class="text-h6 text-h6--mobile">
                  <q-icon v-if="post.is_auto_post" name="history" title="This is a recurring post"/>
                  Post<span v-if="isEmployer"> template</span><span v-if="isEmployees"> by {{ post.user_name }}</span>
                </div>
              </div>
              <div class="col-12 text-small text-grey-8" style="margin-top: -6px;">
                Created at {{ dateTimeUtil.getDateTime(post.created_dt) }}
              </div>
            </div>
          </template>
          <template v-slot:header>
            <q-btn
              v-if="isUserView"
              outline dense icon="share" text-color="grey-8" label="Share or edit"
              class="q-mr-sm"
              @click="openSharePostDialog(post)"
            />
            <q-btn v-if="isEditable" outline dense icon="delete" text-color="negative" @click="deletePost(post)"/>
          </template>
          <template v-slot:body>
            <div class="w-100">
              <div class="q-mb-xs border-bottom-1-gray-100">
                <div class="q-pa-sm">
                  <div style="display: inline-block;">
                    <span class="copy-target" style="display: none">{{ post.formatted_content }}</span>
                    <q-btn
                      v-if="!isEmployer"
                      dense ripple unelevated icon="content_copy"
                      size="sm"
                      @click="dataUtil.copyText"
                    >
                      Copy post text
                    </q-btn>
                  </div>
                  <div class="q-ml-sm" style="display: inline-block;">
                    <span class="copy-target" style="display: none">{{ post.content }}</span>
                    <q-btn
                      dense ripple unelevated icon="content_copy"
                      size="sm"
                      @click="dataUtil.copyText"
                    >
                      Copy post template text
                    </q-btn>
                  </div>
                  <q-btn
                    v-for="file in post.files"
                    dense ripple unelevated icon="file_download"
                    size="sm" type="a"
                    :href="file.url" target="_blank" download
                    class="q-ml-sm"
                  >
                    Download {{ fileUtil.getFileNameFromUrl(file.url) }}
                  </q-btn>
                </div>
              </div>
              <div class="q-pa-md" style="white-space: pre-line;">
                <div class="row">
                  <div class="col-12 col-md-8 q-pr-md-sm">
                    {{ post.formatted_content }}
                    <div v-for="file in post.files" class="q-mt-lg">
                      <img
                        v-if="fileUtil.isImage(file.url)"
                        :src="file.url" :alt="file.title"
                        style="max-height: 150px; max-width: 100%;"
                      >
                      <video
                        v-if="fileUtil.isVideo(file.url)"
                        style="max-height: 150px; max-width: 100%;"
                      >
                        <source :src="file.url">
                      </video>
                    </div>
                  </div>
                  <div class="col-12 col-md-4 q-pl-md-sm border-left-1-gray-100">
                    <template v-if="isEmployer">
                      <div class="text-h5">{{ post.child_posts_count }}</div>
                      <div class="text-grey-7">Employee {{ dataUtil.pluralize('post', post.child_posts_count, false) }}</div>
                    </template>
                    <template v-else>
                      <div class="text-bold">
                        Post history
                        <CustomTooltip icon_size="16px">
                          This shows which platforms you posted to and at what time
                        </CustomTooltip>
                      </div>
                      <ul v-if="post.posts.length">
                        <li v-for="postItem in post.posts" class="text-small">
                          Posted on {{ dateTimeUtil.getDateTime(postItem.posted_dt) }} from
                          {{ postItem.email }} account
                        </li>
                      </ul>
                      <div v-else class="text-small q-mt-sm">
                        Content has not been posted
                      </div>
                    </template>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </CollapsableCard>
      </div>
    </div>
    <q-pagination
      v-if="socialPostPagesCount > 1"
      v-model="pageNumber"
      :max-pages="5"
      :max="socialPostPagesCount"
      direction-links
    />
  </div>
</template>

<script>
import CollapsableCard from 'components/CollapsableCard.vue'
import CustomTooltip from 'components/CustomTooltip.vue'
import DialogShareSocialPost, { loadDialogShareSocialPostFn } from 'components/dialogs/DialogShareSocialPost.vue'
import DateRangeSelector from 'components/inputs/DateRangeSelector.vue'
import SelectEmployee from 'components/inputs/SelectEmployee.vue'
import SelectPlatform from 'components/inputs/SelectPlatform.vue'
import { useQuasar } from 'quasar'
import dataUtil from 'src/utils/data.js'
import dateTimeUtil from 'src/utils/datetime.js'
import fileUtil from 'src/utils/file.js'
import { openConfirmDialog } from 'src/utils/requests.js'
import { useAuthStore } from 'stores/auth-store.js'
import { useContentStore } from 'stores/content-store.js'

export default {
  name: 'SocialPostsSection',
  props: {
    isEmployer: Boolean,
    isUserView: {
      type: Boolean,
      default: true
    },
    isEditable: Boolean
  },
  components: { SelectEmployee, CollapsableCard, CustomTooltip, SelectPlatform, DateRangeSelector },
  data () {
    return {
      isLoaded: false,
      user: null,
      postFilter: {},
      pageNumber: 1,
      dataUtil,
      dateTimeUtil,
      fileUtil
    }
  },
  computed: {
    isEmployees () {
      return !this.isEmployer && !this.isUserView
    },
    socialPostContent () {
      if (!this.user) {
        return {}
      }
      const filterParams = this.getSocialPostFilterParams()
      const postContent = this.contentStore.getSocialPosts(
        (this.isEmployer) ? this.user.employer_id : null,
        (this.isEmployer) ? null : this.user.id,
        this.pageNumber, filterParams, this.isEmployees
      ) || {}
      return postContent
    },
    socialPosts () {
      return this.socialPostContent.posts
    },
    socialPostPagesCount () {
      return this.socialPostContent.total_page_count
    }
  },
  watch: {
    postFilter: {
      async handler () {
        await this.setSocialPosts()
      },
      deep: true
    },
    pageNumber: {
      async handler () {
        await this.setSocialPosts()
      }
    }
  },
  methods: {
    getSocialPostFilterParams () {
      const filterParams = {}
      const startDate = this.postFilter?.dateRange?.from
      if (startDate) {
        filterParams.start_date = dateTimeUtil.serializeDate(startDate, { isIncludeTime: true })
      }
      const endDate = this.postFilter?.dateRange?.to
      if (endDate) {
        filterParams.end_date = dateTimeUtil.serializeDate(endDate, { isIncludeTime: true, isEndOfDay: true })
      }
      if (this.postFilter?.platforms?.length) {
        filterParams.platform_ids = this.postFilter.platforms.map((p) => p.id)
      }
      if (this.postFilter?.employee_ids?.length) {
        filterParams.employee_ids = this.postFilter.employee_ids
      }
      return filterParams
    },
    async setSocialPosts (isForceRefresh = false) {
      const kwargs = {
        filterParams: this.getSocialPostFilterParams(),
        isEmployees: this.isEmployees
      }
      if (isForceRefresh) {
        kwargs.isForceRefresh = true
        this.pageNumber = 1
      }
      return await this.contentStore.setSocialPosts(
        (this.isEmployer) ? this.user.employer_id : null,
        (this.isEmployer) ? null : this.user.id,
        this.pageNumber, kwargs
      )
    },
    async deletePost (post) {
      openConfirmDialog(this.q, 'Are you sure you want to delete this post? It will only be deleted from JobVyne. If it has been posted to any social media sites, it will continue to exist there.', {
        okFn: async () => {
          await this.$api.delete(`social-post/${post.id}`)
          await this.setSocialPosts(true)
        }
      })
    },
    async openSharePostDialog (post) {
      await loadDialogShareSocialPostFn()
      return this.q.dialog({
        component: DialogShareSocialPost,
        componentProps: { post }
      }).onOk(() => {
        this.$emit('updatePosts')
      })
    }
  },
  setup () {
    return {
      authStore: useAuthStore(),
      contentStore: useContentStore(),
      q: useQuasar()
    }
  },
  async mounted () {
    await this.authStore.setUser()
    this.user = this.authStore.propUser
    await this.setSocialPosts()
    this.isLoaded = true
  }
}
</script>
